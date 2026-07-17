package com.example.nannaiptv.ui.settings

import android.app.Application
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.material3.*
import com.example.nannaiptv.data.SettingsManager
import kotlinx.coroutines.launch

@Composable
fun SettingsScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val settingsManager = remember { SettingsManager(context) }
    val coroutineScope = rememberCoroutineScope()
    
    val savedUrl by settingsManager.playlistUrlFlow.collectAsState(initial = "")
    var inputUrl by remember { mutableStateOf("") }
    
    // Initialize text field with saved URL when it loads
    LaunchedEffect(savedUrl) {
        if (savedUrl != null) {
            inputUrl = savedUrl!!
        }
    }

    BackHandler(onBack = onBack)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(48.dp)
    ) {
        Column(
            modifier = Modifier.fillMaxWidth(0.6f)
        ) {
            Text(
                text = "Settings",
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onBackground,
                modifier = Modifier.padding(bottom = 32.dp)
            )

            Text(
                text = "M3U Playlist URL",
                fontSize = 18.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(bottom = 8.dp)
            )

            // Note: Standard TextField isn't perfectly optimized for TV out-of-the-box, 
            // but we use a workaround or standard compose TextField for now.
            // A production TV app might use a custom Keyboard or pin sync.
            androidx.compose.material3.OutlinedTextField(
                value = inputUrl,
                onValueChange = { inputUrl = it },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 24.dp),
                placeholder = { Text("http://example.com/playlist.m3u8") },
                singleLine = true,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done)
            )

            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(
                    onClick = {
                        coroutineScope.launch {
                            settingsManager.savePlaylistUrl(inputUrl)
                        }
                    },
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(imageVector = Icons.Default.Refresh, contentDescription = null, modifier = Modifier.padding(end = 8.dp))
                    Text("Save & Reload")
                }

                OutlinedButton(
                    onClick = {
                        coroutineScope.launch {
                            settingsManager.clearPlaylistUrl()
                            inputUrl = ""
                        }
                    },
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(imageVector = Icons.Default.Delete, contentDescription = null, modifier = Modifier.padding(end = 8.dp))
                    Text("Clear to Default")
                }
            }

            Spacer(modifier = Modifier.height(48.dp))

            Text(
                text = "Note: Typing a full URL on a TV remote can be tedious. A feature to pair via a mobile app short-code can be added here in the future.",
                fontSize = 14.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
