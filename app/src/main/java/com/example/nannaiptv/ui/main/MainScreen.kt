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
import androidx.tv.foundation.lazy.list.items
import androidx.tv.material3.*
import com.example.nannaiptv.data.DefaultDataRepository
import com.example.nannaiptv.data.DefaultChannelData
import com.example.nannaiptv.data.Channel

@Composable
fun MainScreen(
    onItemClick: (NavKey) -> Unit,
    modifier: Modifier = Modifier,
    viewModel: MainScreenViewModel = viewModel { MainScreenViewModel(DefaultDataRepository()) },
) {
    // Load real data
    val categoryMap = DefaultChannelData.flattenedCategories
    val categoryNames = categoryMap.keys.toList()
    
    var selectedCategoryName by remember { mutableStateOf(categoryNames.firstOrNull() ?: "") }
    var showActive by remember { mutableStateOf(true) }

    // Get channels for the selected category, filtered by Active/Inactive
    val channelsForCategory = categoryMap[selectedCategoryName] ?: emptyList()
    val displayedChannels = channelsForCategory.filter { it.isActive == showActive }

    Row(modifier = modifier.fillMaxSize().background(Color(0xFFF0F0F0))) {
        // Left Sidebar (Categories)
        Box(
            modifier = Modifier
                .width(280.dp)
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
                    items(categoryNames) { categoryName ->
                        val isSelected = categoryName == selectedCategoryName
                        Surface(
                            onClick = { selectedCategoryName = categoryName },
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
                                text = categoryName,
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
            // Tabs Row
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
