package com.example.nannaiptv.ui.main

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
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

@Composable
fun MainScreen(
    onItemClick: (NavKey) -> Unit,
    modifier: Modifier = Modifier,
    viewModel: MainScreenViewModel = viewModel { MainScreenViewModel(DefaultDataRepository()) },
) {
    // 1. Load Data
    val allCategories = DefaultChannelData.categories
    
    // State: Selected Language (Main Category)
    var selectedLanguage by remember { mutableStateOf(allCategories.firstOrNull()?.language ?: "") }
    val currentCategory = allCategories.find { it.language == selectedLanguage }
    
    // State: Selected Genre (Sub Category)
    val availableGenres = currentCategory?.subCategories ?: emptyList()
    var selectedGenre by remember { mutableStateOf(availableGenres.firstOrNull()?.genre ?: "") }
    
    // Auto-update genre if language changes and the old genre doesn't exist
    LaunchedEffect(selectedLanguage) {
        val newAvailableGenres = allCategories.find { it.language == selectedLanguage }?.subCategories ?: emptyList()
        if (newAvailableGenres.none { it.genre == selectedGenre }) {
            selectedGenre = newAvailableGenres.firstOrNull()?.genre ?: ""
        }
    }

    // State: Active/Inactive Filter
    var showActive by remember { mutableStateOf(true) }

    // Final Channels to Display
    val currentSubCategory = availableGenres.find { it.genre == selectedGenre }
    val displayedChannels = currentSubCategory?.channels?.filter { it.isActive == showActive } ?: emptyList()

    Row(modifier = modifier.fillMaxSize().background(Color(0xFFF0F0F0))) {
        // TIER 1: Left Sidebar (Main Categories / Languages)
        Box(
            modifier = Modifier
                .width(260.dp)
                .fillMaxHeight()
                .background(Color.White)
                .padding(16.dp)
        ) {
            Column {
                Text(
                    text = "Nanna IPTV",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black,
                    modifier = Modifier.padding(bottom = 24.dp, start = 16.dp)
                )

                TvLazyColumn {
                    items(allCategories) { category ->
                        val isSelected = category.language == selectedLanguage
                        Surface(
                            onClick = { selectedLanguage = category.language },
                            shape = ClickableSurfaceDefaults.shape(shape = RoundedCornerShape(8.dp)),
                            colors = ClickableSurfaceDefaults.colors(
                                containerColor = if (isSelected) Color(0xFFE0E0E0) else Color.Transparent,
                                contentColor = Color.Black,
                                focusedContainerColor = Color(0xFF2196F3),
                                focusedContentColor = Color.White
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
                            containerColor = if (isSelected) Color(0xFFD0D0D0) else Color.White,
                            contentColor = Color.Black,
                            focusedContainerColor = Color(0xFF2196F3),
                            focusedContentColor = Color.White
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
                        color = if (showActive) Color(0xFF2196F3) else Color.Gray,
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
                        color = if (!showActive) Color(0xFF2196F3) else Color.Gray,
                        fontWeight = if (!showActive) FontWeight.Bold else FontWeight.Normal
                    )
                }
            }

            // 6-Column Channel Grid
            if (displayedChannels.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text("No channels available in this category.", color = Color.Gray, fontSize = 18.sp)
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
                            onClick = { /* Launch ExoPlayer */ },
                            shape = ClickableSurfaceDefaults.shape(shape = RoundedCornerShape(12.dp)),
                            colors = ClickableSurfaceDefaults.colors(
                                containerColor = Color.White,
                                contentColor = Color.Black,
                                focusedContainerColor = Color(0xFF2196F3),
                                focusedContentColor = Color.White
                            ),
                            modifier = Modifier.aspectRatio(16f / 9f) // Standard TV Thumbnail aspect ratio
                        ) {
                            Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxSize().padding(8.dp)) {
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
