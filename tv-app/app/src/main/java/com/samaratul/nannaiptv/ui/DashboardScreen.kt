package com.samaratul.nannaiptv.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.foundation.lazy.list.TvLazyColumn
import androidx.tv.foundation.lazy.list.TvLazyRow
import androidx.tv.foundation.lazy.list.items
import androidx.tv.material3.*
import coil.compose.AsyncImage
import com.samaratul.nannaiptv.data.Channel
import com.samaratul.nannaiptv.data.LanguageGroup

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
            .background(
                brush = Brush.verticalGradient(
                    colors = listOf(
                        Color(0xFF0F172A), // Midnight Blue
                        Color(0xFF020617)  // Deepest Dark
                    )
                )
            )
    ) {
        // Sidebar for Languages (Sleek Glass Panel)
        Box(
            modifier = Modifier
                .width(220.dp)
                .fillMaxHeight()
                .background(Color.White.copy(alpha = 0.03f))
                .padding(20.dp)
        ) {
            TvLazyColumn(
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                item {
                    Text(
                        text = "Nanna IPTV",
                        style = MaterialTheme.typography.headlineSmall.copy(
                            fontWeight = FontWeight.ExtraBold,
                            letterSpacing = 1.sp
                        ),
                        color = Color(0xFF60A5FA), // Neon Blue accent
                        modifier = Modifier.padding(bottom = 24.dp, top = 8.dp)
                    )
                }
                items(languageGroups.size) { index ->
                    val group = languageGroups[index]
                    var isFocused by remember { mutableStateOf(false) }
                    val scale by animateFloatAsState(if (isFocused) 1.05f else 1f, label = "sidebar_scale")

                    Surface(
                        onClick = { selectedLanguageIndex = index },
                        shape = ClickableSurfaceDefaults.shape(shape = RoundedCornerShape(12.dp)),
                        colors = ClickableSurfaceDefaults.colors(
                            containerColor = if (selectedLanguageIndex == index) Color.White.copy(alpha = 0.1f) else Color.Transparent,
                            focusedContainerColor = Color(0xFF3B82F6),
                            contentColor = if (selectedLanguageIndex == index) Color.White else Color.LightGray,
                            focusedContentColor = Color.White
                        ),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(54.dp)
                            .scale(scale)
                            .onFocusChanged { isFocused = it.isFocused }
                    ) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.CenterStart) {
                            Text(
                                text = group.language,
                                style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Medium),
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
                .padding(start = 32.dp, top = 32.dp, end = 32.dp)
        ) {
            val currentLangGroup = languageGroups.getOrNull(selectedLanguageIndex)
            if (currentLangGroup != null) {
                TvLazyColumn(
                    verticalArrangement = Arrangement.spacedBy(32.dp),
                    contentPadding = PaddingValues(bottom = 32.dp)
                ) {
                    item {
                        Text(
                            text = "${currentLangGroup.language} Channels",
                            style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
                            color = Color.White
                        )
                    }

                    items(currentLangGroup.categories) { category ->
                        Column {
                            Text(
                                text = category.title,
                                style = MaterialTheme.typography.titleMedium.copy(
                                    fontWeight = FontWeight.SemiBold,
                                    letterSpacing = 0.5.sp
                                ),
                                color = Color.White.copy(alpha = 0.7f),
                                modifier = Modifier.padding(bottom = 16.dp, start = 4.dp)
                            )
                            
                            TvLazyRow(
                                horizontalArrangement = Arrangement.spacedBy(20.dp),
                                contentPadding = PaddingValues(start = 4.dp, end = 20.dp, top = 8.dp, bottom = 8.dp)
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
                Text("No channels available.", color = Color.White.copy(alpha = 0.5f))
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
    var isFocused by remember { mutableStateOf(false) }
    val scale by animateFloatAsState(if (isFocused) 1.1f else 1f, label = "card_scale")

    Surface(
        onClick = onClick,
        shape = ClickableSurfaceDefaults.shape(shape = RoundedCornerShape(16.dp)),
        colors = ClickableSurfaceDefaults.colors(
            containerColor = Color(0xFF1E293B).copy(alpha = 0.4f), // Translucent card
            focusedContainerColor = Color(0xFF3B82F6), // Blue glow on focus
            contentColor = Color.White
        ),
        modifier = Modifier
            .width(200.dp)
            .height(140.dp)
            .scale(scale)
            .onFocusChanged { isFocused = it.isFocused }
    ) {
        Box(modifier = Modifier.fillMaxSize()) {
            // Ambient inner gradient for premium depth
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(Color.Transparent, Color.Black.copy(alpha = 0.6f))
                        )
                    )
            )

            Column(
                modifier = Modifier.fillMaxSize().padding(12.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                if (channel.logo.isNotEmpty()) {
                    AsyncImage(
                        model = channel.logo,
                        contentDescription = channel.name,
                        modifier = Modifier
                            .size(72.dp)
                            .padding(bottom = 12.dp),
                        contentScale = ContentScale.Fit
                    )
                } else {
                    Box(
                        modifier = Modifier
                            .size(72.dp)
                            .padding(bottom = 12.dp)
                            .background(Color.White.copy(alpha = 0.1f), shape = RoundedCornerShape(12.dp)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text("TV", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                }
                Text(
                    text = channel.name,
                    style = MaterialTheme.typography.bodyLarge.copy(fontWeight = FontWeight.Medium),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }

            // Sleek Offline Badge
            if (channel.url == "http://offline.stream/playlist.m3u8") {
                Box(
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(8.dp)
                        .background(Color(0xFFEF4444).copy(alpha = 0.9f), shape = RoundedCornerShape(4.dp))
                        .padding(horizontal = 6.dp, vertical = 2.dp)
                ) {
                    Text(
                        text = "OFFLINE",
                        style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Bold, fontSize = 9.sp),
                        color = Color.White
                    )
                }
            }
        }
    }
}
