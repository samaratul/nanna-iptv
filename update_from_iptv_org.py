import os
import re
from m3u_parser import M3uParser

sources = {
    "np": "https://iptv-org.github.io/iptv/countries/np.m3u",
    "in": "https://iptv-org.github.io/iptv/countries/in.m3u",
    "eng": "https://iptv-org.github.io/iptv/languages/eng.m3u",
    "hin": "https://iptv-org.github.io/iptv/languages/hin.m3u",
    "bho": "https://iptv-org.github.io/iptv/languages/bho.m3u"
}

def clean_name(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\[.*?\]', '', name)
    return name.lower().replace(' hd', '').replace(' tv', '').replace(' channel', '').strip()

def build_playlist():
    print("Loading iptv-org databases with m3u_parser...")
    parser = M3uParser(timeout=10, useragent="Mozilla/5.0")
    
    global_streams = []
    bhojpuri_streams = []
    for lang, url in sources.items():
        print(f"Fetching {lang} streams...")
        try:
            parser.parse_m3u(url)
            parser.filter_by('status', 'GOOD')
            streams = parser.get_list()
            global_streams.extend(streams)
            if lang == "bho":
                bhojpuri_streams.extend(streams)
        except Exception as e:
            print(f"Failed to fetch {lang}: {e}")
            
    print(f"Loaded {len(global_streams)} GOOD streams.")
    
    print("Reading baseline playlist...")
    baseline = M3uParser()
    try:
        baseline.parse_m3u('playlist_baseline.m3u8')
    except Exception as e:
        print("Could not read baseline, fallback to current working")
        baseline.parse_m3u('playlist_working.m3u8')
        
    original_streams = baseline.get_list()
    
    # We will group them by their category
    categories = {}
    for stream in original_streams:
        cat = stream.get('group-title', 'Uncategorized')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(stream)
        
    with open('playlist_working.m3u8', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n\n")
        
        for category, channels in categories.items():
            f.write(f"# ======================\n")
            f.write(f"# {category}\n")
            f.write(f"# ======================\n")
            
            for stream in channels:
                channel_name = stream.get('name', 'Unknown')
                target_clean = clean_name(channel_name)
                
                original_url = stream.get('url', '')
                original_logo = stream.get('logo', '')
                
                # Check if original URL is dead or generic
                needs_update = 'offline.stream' in original_url or 'jmp2.uk' in original_url or 'youtube.com' in original_url
                
                best_stream = None
                if needs_update:
                    # Try to find a GOOD replacement from iptv-org
                    for s in global_streams:
                        if clean_name(s.get('name', '')) == target_clean:
                            best_stream = s
                            break
                    if not best_stream:
                        for s in global_streams:
                            if target_clean in clean_name(s.get('name', '')):
                                best_stream = s
                                break
                                
                if best_stream:
                    final_url = best_stream.get('url')
                    final_logo = original_logo if original_logo else best_stream.get('logo', '')
                else:
                    final_url = original_url
                    final_logo = original_logo
                    
                if final_logo:
                    f.write(f'#EXTINF:-1 tvg-logo="{final_logo}" group-title="{category}",{channel_name}\n')
                else:
                    f.write(f'#EXTINF:-1 group-title="{category}",{channel_name}\n')
                f.write(f"{final_url}\n")
            f.write("\n")
            
        # Append all Bhojpuri streams
        if bhojpuri_streams:
            f.write(f"# ======================\n")
            f.write(f"# Bhojpuri - General\n")
            f.write(f"# ======================\n")
            for stream in bhojpuri_streams:
                channel_name = stream.get('name', 'Unknown')
                final_url = stream.get('url', '')
                final_logo = stream.get('logo', '')
                
                if final_logo:
                    f.write(f'#EXTINF:-1 tvg-logo="{final_logo}" group-title="Bhojpuri - General",{channel_name}\n')
                else:
                    f.write(f'#EXTINF:-1 group-title="Bhojpuri - General",{channel_name}\n')
                f.write(f"{final_url}\n")
            f.write("\n")
            
    print("Successfully built playlist_working.m3u8 retaining hardcoded links and appending Bhojpuri.")

if __name__ == "__main__":
    build_playlist()
