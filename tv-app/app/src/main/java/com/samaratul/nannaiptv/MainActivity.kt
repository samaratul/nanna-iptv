package com.samaratul.nannaiptv

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import com.samaratul.nannaiptv.data.Channel
import com.samaratul.nannaiptv.data.LanguageGroup
import com.samaratul.nannaiptv.data.M3uParser
import com.samaratul.nannaiptv.ui.DashboardScreen
import com.samaratul.nannaiptv.ui.PlayerScreen
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val scope = rememberCoroutineScope()
            var languageGroups by remember { mutableStateOf<List<LanguageGroup>?>(null) }
            var selectedChannel by remember { mutableStateOf<Channel?>(null) }
            var isLoading by remember { mutableStateOf(true) }

            LaunchedEffect(Unit) {
                scope.launch {
                    val parser = M3uParser()
                    // Fetch directly from the repository's main branch, appending timestamp to bypass GitHub's 5-minute cache
                    val url = "https://raw.githubusercontent.com/samaratul/nanna-iptv/main/playlist_working.m3u8?t=${System.currentTimeMillis()}"
                    languageGroups = parser.fetchAndParseM3u(url)
                    isLoading = false
                }
            }

            Box(modifier = Modifier.fillMaxSize()) {
                if (isLoading) {
                    CircularProgressIndicator(
                        modifier = Modifier.align(Alignment.Center),
                        color = Color(0xFF3B82F6)
                    )
                } else if (selectedChannel != null) {
                    PlayerScreen(
                        channel = selectedChannel!!,
                        onBackPressed = { selectedChannel = null }
                    )
                } else {
                    languageGroups?.let {
                        DashboardScreen(
                            languageGroups = it,
                            onChannelSelected = { channel ->
                                selectedChannel = channel
                            }
                        )
                    }
                }
            }
        }
    }
}
