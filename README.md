# 📺 Nanna IPTV

A modern, fast, and completely dynamic IPTV player designed specifically for Android TV. Say goodbye to hardcoded channel lists—Nanna IPTV loads your favorite `.m3u` playlists on the fly!

## ✨ Features

- **Modern Android TV UI:** Built 100% with Jetpack Compose for TV (Material 3).
- **Dynamic M3U Parsing:** Just paste a playlist URL, and the app instantly parses all `#EXTINF` metadata (Channel Names, Logos, Categories/Groups, and Stream URLs).
- **Persistent Storage:** Safely stores your configured M3U URL using Jetpack DataStore, so your channels are ready the moment you turn on the TV.
- **Flawless Playback:** Powered by ExoPlayer (AndroidX Media3), natively supporting HLS (`.m3u8`), MPEG-DASH, and HTTP/HTTPS streams.
- **Glassmorphic Design:** Premium, dark-mode focused aesthetic with smooth D-Pad navigation.
- **Web Prototype Included:** Test the layout and M3U parser instantly in your browser before compiling the APK!

## 🚀 Getting Started

### 1. Compile the Android TV App
To build the app and install it on your Android TV or Emulator:
1. Open this project in **Android Studio (Giraffe or newer)**.
2. Let Gradle sync and download all dependencies.
3. Select your Android TV emulator (or physical TV with USB Debugging enabled).
4. Hit **Run** (`Shift + F10`).

### 2. Loading Channels
By default, the app is a blank canvas. To load channels:
1. Navigate to the **Settings** button in the sidebar.
2. Enter a valid `.m3u` playlist URL. 
   *(We provide a community-curated playlist for you! See below).*
3. Click **Save & Restart**. The app will fetch the playlist and dynamically build the categories!

## 🌐 The Official Nanna Playlist

This repository comes with an officially maintained `playlist.m3u` file containing working, free-to-air HD channels across multiple categories (Nepali, Hindi Entertainment, Sports, News, Kids, and more).

**To use it in your app, enter this URL in the Settings:**
```text
https://raw.githubusercontent.com/samaratul/nanna-iptv/main/playlist.m3u
```

Want to add your own channels? Just edit the `playlist.m3u` file in this repository and push the changes. The app will automatically pull the latest channels on its next launch!

## 💻 Web Prototype

Don't want to launch the Android Studio Emulator just to see the UI? We built a pixel-perfect HTML/Tailwind web prototype!

1. Open `web_prototype/index.html` in your favorite browser.
2. The prototype runs actual Javascript to parse the M3U playlist just like the Kotlin app!
3. Go to Settings, paste your M3U URL, and watch the UI magically build itself.

## 🛠 Tech Stack

- **Kotlin**
- **Jetpack Compose for TV (tv-foundation, tv-material)**
- **Jetpack DataStore (Preferences)**
- **AndroidX Media3 (ExoPlayer)**
- **Coil (Image Loading)**
- **Coroutines & Flow**

---
*Built with ❤️ for Android TV.*
