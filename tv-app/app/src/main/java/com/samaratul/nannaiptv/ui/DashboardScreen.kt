package com.samaratul.nannaiptv.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.tv.material3.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.Alignment
import androidx.tv.foundation.lazy.list.TvLazyColumn
import androidx.tv.foundation.lazy.list.TvLazyRow
import androidx.tv.foundation.lazy.list.items
import coil.compose.AsyncImage
import com.samaratul.nannaiptv.data.Channel
import com.samaratul.nannaiptv.data.LanguageGroup
import androidx.compose.ui.layout.ContentScale
import androidx.tv.foundation.lazy.grid.TvLazyVerticalGrid
import androidx.tv.foundation.lazy.grid.TvGridCells
import androidx.tv.foundation.lazy.grid.items

@OptIn(ExperimentalTvMaterial3Api::class)
@Composable
fun DashboardScreen(
    languageGroups: List<LanguageGroup>,
    onChannelSelected: (Channel) -> Unit
) {
    var selectedLanguageIndex by remember { mutableIntStateOf(0) }

    Row(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF0F172A)) // Lumina Cinematic Dark Background
    ) {
        // Sidebar for Languages
        Box(
            modifier = Modifier
                .width(200.dp)
                .fillMaxHeight()
                .background(Color(0xFF1E293B))
                .padding(16.dp)
        ) {
            TvLazyColumn(
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                item {
                    Text(
                        text = "Languages",
                        style = MaterialTheme.typography.titleMedium,
                        color = Color.White,
                        modifier = Modifier.padding(bottom = 16.dp)
                    )
                }
                items(languageGroups.size) { index ->
                    val group = languageGroups[index]
                    Surface(
                        onClick = { selectedLanguageIndex = index },
                        shape = ClickableSurfaceDefaults.shape(shape = RoundedCornerShape(8.dp)),
                        colors = ClickableSurfaceDefaults.colors(
                            containerColor = if (selectedLanguageIndex == index) Color(0xFF3B82F6) else Color.Transparent,
                            focusedContainerColor = Color(0xFF60A5FA),
                            contentColor = Color.White
                        ),
                        modifier = Modifier.fillMaxWidth().height(50.dp)
                    ) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.CenterStart) {
                            Text(
                                text = group.language,
                                modifier = Modifier.padding(start = 16.dp)
                            )
                        }
                    }
                }
            }
        }

        // Main Content Area
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp)
        ) {
            val currentLangGroup = languageGroups.getOrNull(selectedLanguageIndex)
            if (currentLangGroup != null) {
                TvLazyColumn(
                    verticalArrangement = Arrangement.spacedBy(24.dp)
                ) {
                    item {
                        Text(
                            text = "${currentLangGroup.language} Channels",
                            style = MaterialTheme.typography.headlineMedium,
                            color = Color.White
                        )
                    }

                    items(currentLangGroup.categories) { category ->
                        Column {
                            Text(
                                text = category.title,
                                style = MaterialTheme.typography.titleMedium,
                                color = Color.LightGray,
                                modifier = Modifier.padding(bottom = 12.dp)
                            )
                            
                            TvLazyRow(
                                horizontalArrangement = Arrangement.spacedBy(16.dp)
                            ) {
                                items(category.channels) { channel ->
                                    ChannelCard(
                                        channel = channel,
                                        onClick = { onChannelSelected(channel) }
                                    )
                                }
                            }
                        }
                    }
                }
            } else {
                Text("No channels available.", color = Color.White)
            }
        }
    }
}

@OptIn(ExperimentalTvMaterial3Api::class)
@Composable
fun ChannelCard(
    channel: Channel,
    onClick: () -> Unit
) {
    Surface(
        onClick = onClick,
        shape = ClickableSurfaceDefaults.shape(shape = RoundedCornerShape(12.dp)),
        colors = ClickableSurfaceDefaults.colors(
            containerColor = Color(0xFF1E293B),
            focusedContainerColor = Color(0xFF3B82F6),
            contentColor = Color.White
        ),
        modifier = Modifier
            .width(180.dp)
            .height(120.dp)
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            if (channel.logo.isNotEmpty()) {
                AsyncImage(
                    model = channel.logo,
                    contentDescription = channel.name,
                    modifier = Modifier.size(64.dp).padding(bottom = 8.dp),
                    contentScale = ContentScale.Fit
                )
            } else {
                Box(
                    modifier = Modifier
                        .size(64.dp)
                        .padding(bottom = 8.dp)
                        .background(Color.DarkGray, shape = RoundedCornerShape(8.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    Text("TV", color = Color.White)
                }
            }
            Text(
                text = channel.name,
                style = MaterialTheme.typography.bodyMedium,
                maxLines = 1
            )
            if (channel.url == "http://offline.stream/playlist.m3u8") {
                Text(
                    text = "Offline",
                    style = MaterialTheme.typography.labelSmall,
                    color = Color.Red
                )
            }
        }
    }
}
