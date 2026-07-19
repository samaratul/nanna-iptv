import os
import re
from m3u_parser import M3uParser

sources = {
    "np": "https://iptv-org.github.io/iptv/countries/np.m3u",
    "in": "https://iptv-org.github.io/iptv/countries/in.m3u",
    "eng": "https://iptv-org.github.io/iptv/languages/eng.m3u",
    "hin": "https://iptv-org.github.io/iptv/languages/hin.m3u"
}

# The curated structure we want to maintain
TARGET_CHANNELS = [
    ("Nepali - Entertainment", ["Kantipur Max HD", "Nari HD", "Indreni TV", "GNN", "Prime TV"]),
    ("Nepali - Movies", ["A1 TV", "Mega Gold", "Kasthamandap Gold"]),
    ("Nepali - Sports", ["Himalaya Sports HD", "Action Sports HD"]),
    ("Nepali - News", ["Nepal TV HD", "NTV News/Plus HD", "Kantipur HD", "AP1 HD", "Himalaya TV HD", "News 24", "Image HD", "Sagarmatha TV", "Avenues TV", "ABC News", "Mountain TV", "Janata TV", "Channel 4 Nepal"]),
    ("Nepali - Infotainment/Other", ["Indigenous Television", "Nepal Mandal", "Bodhi TV", "Krishi TV", "Business Plus", "Dharma TV", "Deep Television"]),
    ("Hindi - Entertainment", ["Star Plus HD", "Star Bharat HD", "Sony Entertainment (SET) HD", "Sony SAB HD", "Zee TV HD", "Colors HD", "&TV HD", "Colors Rishtey", "Sony Pal", "Star Utsav", "Zee Anmol", "Sony MAX", "Star Gold HD", "Zee Cinema HD", "Colors Cineplex HD", "Utsav Movies", "Sony Wah", "Star Utsav Movies", "Zee Anmol Cinema"]),
    ("Hindi - News", ["Aaj Tak", "NDTV 24x7", "ABP News", "India TV", "News18 India", "Zee News"]),
    ("Hindi - Sports", ["Star Sports 1 HD Hindi", "Star Sports 2 HD", "Sony Sports Ten 1 HD", "Sony Sports Ten 2 HD", "Sony Sports Ten 3 HD", "Sports18 1 HD"]),
    ("Hindi - Kids", ["Cartoon Network India", "Pogo", "Hungama TV", "Disney Channel India", "Nick India"]),
    ("Hindi - Music", ["MTV India", "Zoom", "9xM", "B4U Music"]),
    ("English - News", ["Al Jazeera HD", "India Today", "CNN International", "BBC World News", "France 24", "TRT World HD", "WION", "Republic TV"]),
    ("English - Entertainment", ["Star Movies HD", "Sony Pix HD", "MNX HD", "&flix HD", "Romedy Now", "Comedy Central", "Zee Cafe HD"]),
    ("English - Infotainment", ["Discovery HD", "National Geographic HD", "Animal Planet HD", "History TV18 HD", "Sony BBC Earth HD", "TLC HD"])
]

def clean_name(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\[.*?\]', '', name)
    return name.lower().replace(' hd', '').replace(' tv', '').replace(' channel', '').strip()

def build_playlist():
    print("Loading iptv-org databases with m3u_parser...")
    parser = M3uParser(timeout=10, useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    global_streams = []
    for lang, url in sources.items():
        print(f"Fetching {lang} streams...")
        try:
            parser.parse_m3u(url)
            parser.filter_by('status', 'GOOD')
            global_streams.extend(parser.get_list())
        except Exception as e:
            print(f"Failed to fetch {lang}: {e}")
            
    print(f"Loaded {len(global_streams)} GOOD streams.")
    
    with open('playlist_working.m3u8', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n\n")
        
        for category, channels in TARGET_CHANNELS:
            f.write(f"# ======================\n")
            f.write(f"# {category}\n")
            f.write(f"# ======================\n")
            
            for channel_name in channels:
                target_clean = clean_name(channel_name)
                best_stream = None
                
                # First try exact clean match
                for s in global_streams:
                    if clean_name(s.get('name', '')) == target_clean:
                        best_stream = s
                        break
                        
                # If not found, try partial match
                if not best_stream:
                    for s in global_streams:
                        if target_clean in clean_name(s.get('name', '')):
                            best_stream = s
                            break
                            
                logo = best_stream.get('logo', '') if best_stream else ''
                url = best_stream.get('url', 'http://offline.stream/playlist.m3u8') if best_stream else 'http://offline.stream/playlist.m3u8'
                
                if logo:
                    f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}",{channel_name}\n')
                else:
                    f.write(f'#EXTINF:-1 group-title="{category}",{channel_name}\n')
                f.write(f"{url}\n")
            f.write("\n")
            
    print("Successfully built playlist_working.m3u8 mapped to the curated channel list.")

if __name__ == "__main__":
    build_playlist()
