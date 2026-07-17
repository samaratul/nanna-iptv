package com.example.nannaiptv

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.Modifier
import androidx.tv.material3.MaterialTheme
import com.example.nannaiptv.theme.NannaIPTVTheme
import com.example.nannaiptv.ui.main.MainScreen

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import com.example.nannaiptv.data.Channel
import com.example.nannaiptv.ui.player.PlayerScreen

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            NannaIPTVTheme {
                // Root Container for TV App
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(MaterialTheme.colorScheme.background)
                ) {
                    var activeChannel by remember { mutableStateOf<Channel?>(null) }
                    
                    if (activeChannel == null) {
                        MainScreen(
                            onItemClick = { channel -> activeChannel = channel }
                        )
                    } else {
                        PlayerScreen(
                            channel = activeChannel!!,
                            onBack = { activeChannel = null }
                        )
                    }
                }
            }
        }
    }
}
