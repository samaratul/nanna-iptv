package com.example.nannaiptv.ui.main

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation3.runtime.NavKey
import androidx.tv.foundation.lazy.grid.TvGridCells
import androidx.tv.foundation.lazy.grid.TvLazyVerticalGrid
import androidx.tv.foundation.lazy.grid.items
import androidx.tv.foundation.lazy.list.TvLazyColumn
import androidx.tv.foundation.lazy.list.TvLazyRow
import androidx.tv.foundation.lazy.list.items
import androidx.tv.material3.*
import com.example.nannaiptv.data.DefaultDataRepository
import com.example.nannaiptv.data.DefaultChannelData

import com.example.nannaiptv.data.Channel

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Settings

@Composable
fun MainScreen(
    onItemClick: (Channel) -> Unit,
    onSettingsClick: () -> Unit,
    modifier: Modifier = Modifier,
    viewModel: MainScreenViewModel = viewModel(),
) {
    // 1. Load Data from ViewModel
    val allCategories by viewModel.categories.collectAsStateWithLifecycle()
    val isLoading by viewModel.isLoading.collectAsStateWithLifecycle()
    
    // State: Selected Language (Main Category)
    var selectedLanguage by remember { mutableStateOf("") }
    
    // Initialize selectedLanguage when categories load
    LaunchedEffect(allCategories) {
        if (selectedLanguage.isEmpty() && allCategories.isNotEmpty()) {
            selectedLanguage = allCategories.first().language
        }
    }
    
    val currentCategory = allCategories.find { it.language == selectedLanguage } ?: allCategories.firstOrNull()
    
    // State: Selected Genre (Sub Category)
    val availableGenres = currentCategory?.subCategories ?: emptyList()
    var selectedGenre by remember { mutableStateOf("") }
    
    // Auto-update genre if language changes and the old genre doesn't exist
    LaunchedEffect(selectedLanguage, availableGenres) {
        if (availableGenres.isNotEmpty() && availableGenres.none { it.genre == selectedGenre }) {
            selectedGenre = availableGenres.first().genre
        }
    }

    // State: Active/Inactive Filter
    var showActive by remember { mutableStateOf(true) }

    // Final Channels to Display
    val currentSubCategory = availableGenres.find { it.genre == selectedGenre }
    val displayedChannels = currentSubCategory?.channels?.filter { it.isActive == showActive } ?: emptyList()

    Row(modifier = modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        // TIER 1: Left Sidebar (Main Categories / Languages)
        Box(
            modifier = Modifier
                .width(260.dp)
                .fillMaxHeight()
                .background(MaterialTheme.colorScheme.surfaceContainerLow)
                .padding(16.dp)
        ) {
            Column(modifier = Modifier.fillMaxHeight()) {
                Text(
                    text = "Nanna IPTV",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary, // Glowing cyan brand color
                    modifier = Modifier.padding(bottom = 24.dp, start = 16.dp)
                )

                TvLazyColumn(modifier = Modifier.weight(1f)) {
                    items(allCategories) { category ->
                        val isSelected = category.language == selectedLanguage
                        Surface(
                            onClick = { selectedLanguage = category.language },
                            shape = ClickableSurfaceDefaults.shape(shape = RoundedCornerShape(8.dp)),
                            colors = ClickableSurfaceDefaults.colors(
                                containerColor = if (isSelected) MaterialTheme.colorScheme.surfaceVariant else androidx.compose.ui.graphics.Color.Transparent,
                                contentColor = if (isSelected) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant,
                                focusedContainerColor = MaterialTheme.colorScheme.primary,
                                focusedContentColor = MaterialTheme.colorScheme.onPrimary
                            ),
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)
                        ) {
                            Text(
                                text = category.language,
                                modifier = Modifier.padding(16.dp),
                                fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                            )
                        }
                    }
                }

                // Settings Button at bottom of sidebar
                Surface(
                    onClick = onSettingsClick,
                    shape = ClickableSurfaceDefaults.shape(shape = RoundedCornerShape(8.dp)),
                    colors = ClickableSurfaceDefaults.colors(
                        containerColor = androidx.compose.ui.graphics.Color.Transparent,
                        contentColor = MaterialTheme.colorScheme.onSurfaceVariant,
                        focusedContainerColor = MaterialTheme.colorScheme.primary,
                        focusedContentColor = MaterialTheme.colorScheme.onPrimary
                    ),
                    modifier = Modifier.fillMaxWidth().padding(top = 16.dp)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.padding(16.dp)
                    ) {
                        Icon(imageVector = Icons.Default.Settings, contentDescription = "Settings", modifier = Modifier.padding(end = 12.dp))
                        Text(text = "Settings", fontWeight = FontWeight.Medium)
                    }
                }
            }
        }

        // Main Content Area
        Column(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
                .padding(24.dp)
        ) {
            // TIER 2: Sub-Categories (Genres) Row at the Top
            TvLazyRow(
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(availableGenres) { subCategory ->
                    val isSelected = subCategory.genre == selectedGenre
                    Surface(
                        onClick = { selectedGenre = subCategory.genre },
                        shape = ClickableSurfaceDefaults.shape(shape = RoundedCornerShape(24.dp)),
                        colors = ClickableSurfaceDefaults.colors(
                            containerColor = if (isSelected) MaterialTheme.colorScheme.surfaceVariant else MaterialTheme.colorScheme.surfaceContainer,
                            contentColor = if (isSelected) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant,
                            focusedContainerColor = MaterialTheme.colorScheme.primary,
                            focusedContentColor = MaterialTheme.colorScheme.onPrimary
                        )
                    ) {
                        Text(
                            text = subCategory.genre,
                            modifier = Modifier.padding(horizontal = 24.dp, vertical = 12.dp),
                            fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                        )
                    }
                }
            }

            // TIER 3: Active/Inactive Tabs
            TabRow(
                selectedTabIndex = if (showActive) 0 else 1,
                modifier = Modifier.padding(bottom = 24.dp)
            ) {
                Tab(
                    selected = showActive,
                    onFocus = { showActive = true },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(
                        "Active",
                        color = if (showActive) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                        fontWeight = if (showActive) FontWeight.Bold else FontWeight.Normal
                    )
                }
                Tab(
                    selected = !showActive,
                    onFocus = { showActive = false },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(
                        "Inactive",
                        color = if (!showActive) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                        fontWeight = if (!showActive) FontWeight.Bold else FontWeight.Normal
                    )
                }
            }

            // 6-Column Channel Grid
            if (displayedChannels.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text("No channels available in this category.", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 18.sp)
                }
            } else {
                TvLazyVerticalGrid(
                    columns = TvGridCells.Fixed(6),
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(displayedChannels) { channel -> 
                        Surface(
                            onClick = { onItemClick(channel) },
                            shape = ClickableSurfaceDefaults.shape(shape = RoundedCornerShape(12.dp)),
                            colors = ClickableSurfaceDefaults.colors(
                                containerColor = MaterialTheme.colorScheme.surfaceContainerHigh,
                                contentColor = MaterialTheme.colorScheme.onSurface,
                                focusedContainerColor = MaterialTheme.colorScheme.primary,
                                focusedContentColor = MaterialTheme.colorScheme.onPrimary
                            ),
                            modifier = Modifier.aspectRatio(16f / 9f) // Standard TV Thumbnail aspect ratio
                        ) {
                            Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxSize().padding(8.dp)) {
                                if (channel.logoUrl != null) {
                                    coil.compose.AsyncImage(
                                        model = channel.logoUrl,
                                        contentDescription = channel.name,
                                        modifier = Modifier.fillMaxSize().padding(16.dp)
                                    )
                                } else {
                                    Text(
                                        text = channel.name,
                                        fontWeight = FontWeight.Medium,
                                        textAlign = TextAlign.Center
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
