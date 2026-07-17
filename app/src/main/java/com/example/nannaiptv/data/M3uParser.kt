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
        // We need to re-parse or hold the group during parsing. Let's do it better.
        val parsedData = mutableListOf<ParsedChannel>()
        
        var currentName = ""
        var currentLogoUrl: String? = null
        var currentGroup = "Uncategorized"

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
                            group = currentGroup
                        )
                    )
                }
                currentName = ""
                currentLogoUrl = null
                currentGroup = "Uncategorized"
            }
        }

        // Group by 'group' -> SubCategory
        val subCategories = parsedData.groupBy { it.group }.map { (groupName, channelsList) ->
            SubCategory(
                genre = groupName,
                channels = channelsList.map { 
                    Channel(name = it.name, url = it.url, logoUrl = it.logoUrl, isActive = true) 
                }
            )
        }

        // For simplicity, wrap everything in one main "All" Category since M3U usually doesn't have 2 tiers of categories.
        return listOf(Category(language = "All Channels", subCategories = subCategories))
    }

    private data class ParsedChannel(
        val name: String,
        val url: String,
        val logoUrl: String?,
        val group: String
    )
}
