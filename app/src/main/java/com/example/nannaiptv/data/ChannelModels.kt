package com.example.nannaiptv.data

data class Channel(
    val name: String,
    val url: String = "",
    val logoUrl: String? = null,
    val isActive: Boolean = true
)

data class SubCategory(
    val genre: String,
    val channels: List<Channel>
)

data class Category(
    val language: String,
    val subCategories: List<SubCategory>
)
