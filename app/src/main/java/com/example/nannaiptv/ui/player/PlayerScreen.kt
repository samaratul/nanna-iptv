package com.example.nannaiptv.ui.player

import android.view.ViewGroup
import android.widget.FrameLayout
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import androidx.tv.material3.Text
import com.example.nannaiptv.data.Channel

@Composable
fun PlayerScreen(
    channel: Channel,
    onBack: () -> Unit
) {
    val context = LocalContext.current
    
    // Manage ExoPlayer instance lifecycle
    val exoPlayer = remember {
        ExoPlayer.Builder(context).build().apply {
            playWhenReady = true
        }
    }

    // Set MediaItem when channel URL changes
    LaunchedEffect(channel.url) {
        if (channel.url.isNotBlank()) {
            val mediaItem = MediaItem.fromUri(channel.url)
            exoPlayer.setMediaItem(mediaItem)
            exoPlayer.prepare()
        }
    }

    // Handle TV Back Button
    BackHandler(onBack = onBack)

    // Release player when screen is destroyed
    DisposableEffect(Unit) {
        onDispose {
            exoPlayer.release()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black),
        contentAlignment = Alignment.Center
    ) {
        if (channel.url.isBlank()) {
            Text(
                text = "Stream URL is not available for ${channel.name}",
                color = Color.White
            )
        } else {
            AndroidView(
                factory = { ctx ->
                    PlayerView(ctx).apply {
                        player = exoPlayer
                        useController = true
                        layoutParams = FrameLayout.LayoutParams(
                            ViewGroup.LayoutParams.MATCH_PARENT,
                            ViewGroup.LayoutParams.MATCH_PARENT
                        )
                    }
                },
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}
