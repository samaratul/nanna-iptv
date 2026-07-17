package com.example.nannaiptv.data

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")

class SettingsManager(private val context: Context) {

    companion object {
        val PLAYLIST_URL_KEY = stringPreferencesKey("playlist_url")
    }

    // Get the playlist URL as a flow
    val playlistUrlFlow: Flow<String?> = context.dataStore.data
        .map { preferences ->
            preferences[PLAYLIST_URL_KEY]
        }

    // Save the playlist URL
    suspend fun savePlaylistUrl(url: String) {
        context.dataStore.edit { preferences ->
            preferences[PLAYLIST_URL_KEY] = url
        }
    }

    // Clear the playlist URL
    suspend fun clearPlaylistUrl() {
        context.dataStore.edit { preferences ->
            preferences.remove(PLAYLIST_URL_KEY)
        }
    }
}
