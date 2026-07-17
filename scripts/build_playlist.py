import urllib.request
import re
import os

target_channels = {
    # Hindi Entertainment
    "Star Plus": "Entertainment", "Sony Entertainment": "Entertainment", "Colors TV": "Entertainment", "Zee TV": "Entertainment", "SAB TV": "Entertainment",
    # Hindi Movies
    "Star Gold": "Movies", "Sony Max": "Movies", "Zee Cinema": "Movies", "Colors Cineplex": "Movies", "B4U Movies": "Movies",
    # English News
    "BBC News": "News", "BBC World News": "News", "CNN": "News", "Al Jazeera": "News", "Sky News": "News", "Bloomberg": "News", "CNA": "News", "WION": "News",
    # English Movies & Entertainment
    "HBO": "Movies", "Star Movies": "Movies", "AXN": "Entertainment", "Warner TV": "Movies",
    # Sports
    "Star Sports": "Sports", "Sony Ten": "Sports", "Eurosport": "Sports", "Sky Sports": "Sports", "Red Bull TV": "Sports",
    # Kids
    "Cartoon Network": "Kids", "Disney": "Kids", "Nickelodeon": "Kids", "Pogo": "Kids",
    # Infotainment
    "Discovery": "Documentary", "National Geographic": "Documentary", "History": "Documentary", "Animal Planet": "Documentary",
    # Music
    "MTV": "Music", "9XM": "Music", "Zoom": "Music", "Vevo": "Music"
}

sources = [
    "https://iptv-org.github.io/iptv/countries/in.m3u",
    "https://iptv-org.github.io/iptv/countries/us.m3u",
    "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "https://iptv-org.github.io/iptv/categories/news.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "https://iptv-org.github.io/iptv/categories/movies.m3u",
    "https://iptv-org.github.io/iptv/categories/kids.m3u",
    "https://iptv-org.github.io/iptv/categories/music.m3u",
    "https://iptv-org.github.io/iptv/categories/documentary.m3u"
]

found_channels = {}

for source in sources:
    try:
        req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
        content = urllib.request.urlopen(req).read().decode('utf-8')
        lines = content.split('\n')
        
        current_extinf = None
        for line in lines:
            if line.startswith('#EXTINF'):
                current_extinf = line
            elif line.startswith('http') and current_extinf:
                # check if it matches target channels
                for target, group in target_channels.items():
                    # We want to match whole words or exact phrases in the EXTINF line
                    # EXTINF format: #EXTINF:-1 tvg-id="..." tvg-logo="..." group-title="...",Channel Name
                    channel_name_part = current_extinf.split(',')[-1]
                    if target.lower() in channel_name_part.lower():
                        if target not in found_channels:
                            # Update group-title to match our category
                            extinf_clean = re.sub(r'group-title="[^"]*"', f'group-title="{group}"', current_extinf)
                            # if no group-title exists, add it
                            if 'group-title=' not in extinf_clean:
                                extinf_clean = extinf_clean.replace(',', f' group-title="{group}",', 1)
                            
                            found_channels[target] = (extinf_clean, line)
                        break
                current_extinf = None
    except Exception as e:
        print(f"Error fetching {source}: {e}")

# Load existing nepali channels from playlist.m3u
existing_content = ""
try:
    with open("playlist.m3u", "r", encoding="utf-8") as f:
        existing_content = f.read()
except:
    pass

with open("playlist.m3u", "w", encoding="utf-8") as f:
    if not existing_content.startswith("#EXTM3U"):
        f.write("#EXTM3U\n")
    else:
        f.write(existing_content.strip() + "\n\n")
        
    for target, (extinf, url) in found_channels.items():
        f.write(f"{extinf}\n{url}\n\n")

print(f"Added {len(found_channels)} international channels to playlist.m3u!")
