import urllib.request
import re
import os

target_channels = {
    # Hindi Entertainment
    "Star Plus": ("Hindi", "Entertainment"), "Sony Entertainment": ("Hindi", "Entertainment"), "Colors TV": ("Hindi", "Entertainment"), "Zee TV": ("Hindi", "Entertainment"), "SAB TV": ("Hindi", "Entertainment"),
    # Hindi Movies
    "Star Gold": ("Hindi", "Movies"), "Sony Max": ("Hindi", "Movies"), "Zee Cinema": ("Hindi", "Movies"), "Colors Cineplex": ("Hindi", "Movies"), "B4U Movies": ("Hindi", "Movies"),
    # English News
    "BBC News": ("English", "News"), "BBC World News": ("English", "News"), "CNN": ("English", "News"), "Al Jazeera": ("English", "News"), "Sky News": ("English", "News"), "Bloomberg": ("English", "News"), "CNA": ("English", "News"), "WION": ("English", "News"),
    # English Movies & Entertainment
    "HBO": ("English", "Movies"), "Star Movies": ("English", "Movies"), "AXN": ("English", "Entertainment"), "Warner TV": ("English", "Movies"),
    # Sports
    "Star Sports": ("English", "Sports"), "Sony Ten": ("English", "Sports"), "Eurosport": ("English", "Sports"), "Sky Sports": ("English", "Sports"), "Red Bull TV": ("English", "Sports"),
    # Kids
    "Cartoon Network": ("English", "Kids"), "Disney": ("English", "Kids"), "Nickelodeon": ("English", "Kids"), "Pogo": ("English", "Kids"),
    # Infotainment
    "Discovery": ("English", "Documentary"), "National Geographic": ("English", "Documentary"), "History": ("English", "Documentary"), "Animal Planet": ("English", "Documentary"),
    # Music
    "MTV": ("English", "Music"), "9XM": ("Hindi", "Music"), "Zoom": ("Hindi", "Music"), "Vevo": ("English", "Music")
}

nepali_channels = [
    {"name": "Kantipur TV HD", "url": "https://ktvhdsg.ekantipur.com:8443/high_quality_85840165/hd/playlist.m3u8", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d7/Kantipur_Television_logo.svg/512px-Kantipur_Television_logo.svg.png", "genre": "Entertainment"},
    {"name": "AP1 TV HD", "url": "http://maxotts.maxdigitaltv.com/x-media/C22/master.m3u8", "logo": "https://upload.wikimedia.org/wikipedia/en/c/c6/AP1_TV_LOGO.png", "genre": "Entertainment"},
    {"name": "News 24 HD", "url": "http://maxotts.maxdigitaltv.com/x-media/C9/master.m3u8", "logo": "https://i.imgur.com/7PgAPMU.png", "genre": "News"},
    {"name": "Capital TV HD", "url": "https://streaming.tvnepal.com:19360/capitaltv/capitaltv.m3u8", "logo": "https://i.imgur.com/hb4bq1t.png", "genre": "News"},
    {"name": "City One Television HD", "url": "http://maxotts.maxdigitaltv.com/x-media/C209/master.m3u8", "logo": "https://i.imgur.com/AxBreI5.png", "genre": "Entertainment"},
    {"name": "METV HD", "url": "http://maxotts.maxdigitaltv.com/x-media/C168/master.m3u8", "logo": "https://i.imgur.com/Zud862h.png", "genre": "Entertainment"},
    {"name": "Nepal 1", "url": "https://d1msejlow1t3l4.cloudfront.net/fta/nepal1/chunks.m3u8", "logo": "https://i.imgur.com/Xr4FjC8.png", "genre": "Entertainment"},
    {"name": "Mithila Nepal TV HD", "url": "http://150.107.205.212:1935/live/mithila/playlist.m3u8", "logo": "https://i.ibb.co/CWn3fH9/1689333550464.jpg", "genre": "Entertainment"},
    {"name": "Dhaulagiri Television", "url": "http://maxotts.maxdigitaltv.com/x-media/C117/master.m3u8", "logo": "https://i.imgur.com/1tTudCH.png", "genre": "News"}
]

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
                for target, (lang, group) in target_channels.items():
                    channel_name_part = current_extinf.split(',')[-1]
                    if target.lower() in channel_name_part.lower():
                        if target not in found_channels:
                            extinf_clean = re.sub(r'group-title="[^"]*"', f'group-title="{group}"', current_extinf)
                            if 'group-title=' not in extinf_clean:
                                extinf_clean = extinf_clean.replace(',', f' group-title="{group}",', 1)
                            # Add tvg-language
                            extinf_clean = extinf_clean.replace('#EXTINF:-1', f'#EXTINF:-1 tvg-language="{lang}"')
                            found_channels[target] = (extinf_clean, line)
                        break
                current_extinf = None
    except Exception as e:
        print(f"Error fetching {source}: {e}")

with open("../playlist.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for ch in nepali_channels:
        f.write(f'#EXTINF:-1 tvg-language="Nepali" tvg-logo="{ch["logo"]}" group-title="{ch["genre"]}",{ch["name"]}\n{ch["url"]}\n\n')
    for target, (extinf, url) in found_channels.items():
        f.write(f"{extinf}\n{url}\n\n")

print(f"Added Nepali and {len(found_channels)} international channels to playlist.m3u!")
