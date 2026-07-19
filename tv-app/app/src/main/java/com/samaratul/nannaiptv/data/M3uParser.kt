package com.samaratul.nannaiptv.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL

class M3uParser {

    suspend fun fetchAndParseM3u(urlStr: String): List<LanguageGroup> = withContext(Dispatchers.IO) {
        val channels = mutableListOf<Channel>()
        try {
            val url = URL(urlStr)
            val connection = url.openConnection() as HttpURLConnection
            connection.requestMethod = "GET"
            
            val reader = BufferedReader(InputStreamReader(connection.inputStream))
            var line: String?
            
            var currentLanguage = "Unknown"
            var currentCategory = "Unknown"
            var currentName = ""
            var currentLogo = ""
            
            while (reader.readLine().also { line = it } != null) {
                val currentLine = line!!.trim()
                if (currentLine.startsWith("#EXTINF")) {
                    // Extract group-title for Language and Category
                    val groupMatch = Regex("""group-title="([^"]+)"""").find(currentLine)
                    if (groupMatch != null) {
                        val group = groupMatch.groupValues[1]
                        if (group.contains(" - ")) {
                            val parts = group.split(" - ", limit = 2)
                            currentLanguage = parts[0].trim()
                            currentCategory = parts[1].trim()
                        } else {
                            currentLanguage = group.trim()
                            currentCategory = "General"
                        }
                    }
                    
                    // Extract tvg-logo
                    val logoMatch = Regex("""tvg-logo="([^"]+)"""").find(currentLine)
                    if (logoMatch != null) {
                        currentLogo = logoMatch.groupValues[1]
                    } else {
                        currentLogo = ""
                    }
                    
                    // Extract channel name (after the last comma)
                    currentName = currentLine.substringAfterLast(",").trim()
                    
                } else if (currentLine.startsWith("http")) {
                    if (currentName.isNotEmpty()) {
                        channels.add(
                            Channel(
                                name = currentName,
                                url = currentLine,
                                logo = currentLogo,
                                language = currentLanguage,
                                category = currentCategory
                            )
                        )
                        currentName = ""
                        currentLogo = ""
                    }
                }
            }
            reader.close()
        } catch (e: Exception) {
            e.printStackTrace()
        }
        
        // Now group the flat list of channels into LanguageGroup -> CategoryGroup
        val grouped = channels.groupBy { it.language }
            .map { (language, langChannels) ->
                val categories = langChannels.groupBy { it.category }
                    .map { (category, catChannels) ->
                        CategoryGroup(category, catChannels)
                    }
                LanguageGroup(language, categories)
            }
            
        return@withContext grouped
    }
}
