package com.example.nannaiptv.data

import io.ktor.client.HttpClient
import io.ktor.client.request.get
import io.ktor.client.statement.bodyAsText
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class M3uParser(private val client: HttpClient) {

    suspend fun fetchAndParse(url: String): List<Category> = withContext(Dispatchers.IO) {
        try {
            val response = client.get(url)
            val playlistText = response.bodyAsText()
            parseM3u(playlistText)
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }

    private fun parseM3u(m3uContent: String): List<Category> {
        val lines = m3uContent.lines()
        val channels = mutableListOf<Channel>()
        var currentName = ""
        var currentLogoUrl: String? = null
        var currentGroup = "Uncategorized"

        for (line in lines) {
            val trimmed = line.trim()
            if (trimmed.startsWith("#EXTINF:")) {
                // Extract group-title
                val groupTitleMatch = Regex("""group-title="([^"]+)"""").find(trimmed)
                if (groupTitleMatch != null) {
                    currentGroup = groupTitleMatch.groupValues[1]
                }

                // Extract tvg-logo
                val logoMatch = Regex("""tvg-logo="([^"]+)"""").find(trimmed)
                if (logoMatch != null) {
                    currentLogoUrl = logoMatch.groupValues[1]
                }

                // Extract channel name (everything after the last comma)
                val commaIndex = trimmed.lastIndexOf(',')
                if (commaIndex != -1 && commaIndex < trimmed.length - 1) {
                    currentName = trimmed.substring(commaIndex + 1).trim()
                }
            } else if (trimmed.isNotEmpty() && !trimmed.startsWith("#")) {
                // This is the URL line
                if (currentName.isNotEmpty()) {
                    channels.add(
                        Channel(
                            name = currentName,
                            url = trimmed,
                            logoUrl = currentLogoUrl,
                            isActive = true
                        )
                    )
                }
                
                // Reset for next channel
                currentName = ""
                currentLogoUrl = null
                currentGroup = "Uncategorized"
            }
        }

        // Group channels by their group-title (Genre)
        val groupedByGenre = channels.groupBy { it.group } 
        // Note: Channel doesn't have a group property yet, we need to map this properly.
        // Let's create a temporary structure.
        return buildCategories(channels, lines)
    }

    private fun buildCategories(channels: List<Channel>, m3uContent: List<String>): List<Category> {
        val parsedData = mutableListOf<ParsedChannel>()
        
        var currentName = ""
        var currentLogoUrl: String? = null
        var currentGroup = "General"
        var currentLanguage = "Global"

        for (line in m3uContent) {
            val trimmed = line.trim()
            if (trimmed.startsWith("#EXTINF:")) {
                val groupTitleMatch = Regex("""group-title="([^"]+)"""").find(trimmed)
                if (groupTitleMatch != null) {
                    currentGroup = groupTitleMatch.groupValues[1]
                }

                val logoMatch = Regex("""tvg-logo="([^"]+)"""").find(trimmed)
                if (logoMatch != null) {
                    currentLogoUrl = logoMatch.groupValues[1]
                }

                val langMatch = Regex("""tvg-language="([^"]+)"""").find(trimmed)
                if (langMatch != null) {
                    currentLanguage = langMatch.groupValues[1]
                }

                val commaIndex = trimmed.lastIndexOf(',')
                if (commaIndex != -1 && commaIndex < trimmed.length - 1) {
                    currentName = trimmed.substring(commaIndex + 1).trim()
                }
            } else if (trimmed.isNotEmpty() && !trimmed.startsWith("#")) {
                if (currentName.isNotEmpty()) {
                    parsedData.add(
                        ParsedChannel(
                            name = currentName,
                            url = trimmed,
                            logoUrl = currentLogoUrl,
                            group = currentGroup,
                            language = currentLanguage
                        )
                    )
                }
                currentName = ""
                currentLogoUrl = null
                currentGroup = "General"
                currentLanguage = "Global"
            }
        }

        // Group by 'language' -> Category
        val categories = parsedData.groupBy { it.language }.map { (langName, channelsInLang) ->
            // Within each language, group by 'group' (genre) -> SubCategory
            val subCategories = channelsInLang.groupBy { it.group }.map { (groupName, channelsInGroup) ->
                SubCategory(
                    genre = groupName,
                    channels = channelsInGroup.map { 
                        Channel(name = it.name, url = it.url, logoUrl = it.logoUrl, isActive = true) 
                    }
                )
            }
            Category(language = langName, subCategories = subCategories)
        }

        return categories.sortedBy { if (it.language == "Nepali") 0 else 1 }
    }

    private data class ParsedChannel(
        val name: String,
        val url: String,
        val logoUrl: String?,
        val group: String,
        val language: String
    )
}
