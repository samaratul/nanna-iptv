package com.example.nannaiptv

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.width
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            // Root Container for TV App
            Row(modifier = Modifier.fillMaxSize().background(Color(0xFFF0F0F0))) { // Clean Light Theme
                // Sidebar for Categories
                Box(
                    modifier = Modifier
                        .width(250.dp)
                        .fillMaxSize()
                        .background(Color(0xFFFFFFFF)) // White sidebar
                ) {
                    // Category list will go here
                }
                
                // Main Content Area (Tabs + 6-Column Grid)
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .weight(1f)
                        .background(Color(0xFFF0F0F0)) // Light gray main content
                ) {
                    // Tabs (Active/Inactive) and TvLazyVerticalGrid will go here
                }
            }
        }
    }
}
