package com.example.nannaiptv.ui.main

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.nannaiptv.data.Category
import com.example.nannaiptv.data.DefaultChannelData
import com.example.nannaiptv.data.M3uParser
import com.example.nannaiptv.data.SettingsManager
import io.ktor.client.HttpClient
import io.ktor.client.engine.android.Android
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class MainScreenViewModel(application: Application) : AndroidViewModel(application) {

    private val settingsManager = SettingsManager(application)
    private val httpClient = HttpClient(Android)
    private val m3uParser = M3uParser(httpClient)

    private val _categories = MutableStateFlow<List<Category>>(emptyList())
    val categories: StateFlow<List<Category>> = _categories

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> = _isLoading

    init {
        loadData()
    }

    private fun loadData() {
        viewModelScope.launch {
            settingsManager.playlistUrlFlow.collectLatest { url ->
                _isLoading.value = true
                if (url.isNullOrBlank()) {
                    // Fallback to defaults if no custom URL
                    _categories.value = DefaultChannelData.categories
                } else {
                    // Fetch and parse the remote M3U
                    val parsedCategories = m3uParser.fetchAndParse(url)
                    if (parsedCategories.isNotEmpty()) {
                        _categories.value = parsedCategories
                    } else {
                        // Fallback if parsing failed
                        _categories.value = DefaultChannelData.categories
                    }
                }
                _isLoading.value = false
            }
        }
    }

    override fun onCleared() {
        super.onCleared()
        httpClient.close()
    }
}
