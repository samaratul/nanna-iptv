package com.samaratul.nannaiptv.data

data class Channel(
    val name: String,
    val url: String,
    val logo: String,
    val language: String,
    val category: String,
    val isPlaceholder: Boolean = false
)

data class CategoryGroup(
    val title: String,
    val channels: List<Channel>
)

data class LanguageGroup(
    val language: String,
    val categories: List<CategoryGroup>
)
