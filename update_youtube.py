import os
import re
import urllib.request
import yt_dlp

YOUTUBE_CHANNELS = {
    'Aaj Tak': 'https://www.youtube.com/channel/UCt4t-jeY85JegMlZ-E5UWtA/live',
    'ABP News': 'https://www.youtube.com/channel/UCRWFSbif-RFENbBrSiez1DA/live',
    'Al Jazeera HD': 'https://www.youtube.com/aljazeeraenglish/live',
    'France 24': 'https://www.youtube.com/@France24_en/live',
    'TRT World HD': 'https://www.youtube.com/c/trtworld/live',
    'Kantipur Max HD': 'https://www.youtube.com/channel/UC3yDoaqQzOd1bNP74ZrGPTA/live',
    'Kantipur HD': 'https://www.youtube.com/channel/UC3yDoaqQzOd1bNP74ZrGPTA/live',
    'Kantipur TV HD': 'https://www.youtube.com/channel/UC3yDoaqQzOd1bNP74ZrGPTA/live',
    'NDTV 24x7': 'https://www.youtube.com/@NDTV/live',
    'India Today': 'https://www.youtube.com/@indiatoday/live',
    'News 24': 'https://www.youtube.com/@news24tvchannel/live'
}

def clean_channel_name(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\[.*?\]', '', name)
    name = name.lower().replace(' hd', '').replace(' tv', '').replace(' channel', '').strip()
    name = re.sub(r'\s+', ' ', name)
    return name

def fetch_m3u_dict(url):
    print(f"Fetching {url}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req).read().decode('utf-8')
        lines = data.split('\n')
        channels = {}
        current_name = None
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.startswith('#EXTINF:'):
                name_match = re.search(r',(.*)$', line)
                if name_match:
                    current_name = name_match.group(1).strip()
            elif not line.startswith('#') and current_name:
                clean = clean_channel_name(current_name)
                if clean not in channels:
                    channels[clean] = line
                current_name = None
        return channels
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return {}

def extract_youtube_m3u8(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'simulate': True,
        'forceurl': True,
        'nocheckcertificate': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']
    except Exception as e:
        print(f"YouTube extract failed for {url}: {e}")
        return None

def process_m3u(file_path):
    nepali_data = fetch_m3u_dict("https://iptv-org.github.io/iptv/countries/np.m3u")
    indian_data = fetch_m3u_dict("https://iptv-org.github.io/iptv/countries/in.m3u")
    english_data = fetch_m3u_dict("https://iptv-org.github.io/iptv/languages/eng.m3u")
    global_data = fetch_m3u_dict("https://iptv-org.github.io/iptv/index.m3u")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('#EXTINF:'):
            name_match = re.search(r',(.*)$', line)
            group_match = re.search(r'group-title="(.*?)"', line)
            new_lines.append(line)
            
            i += 1
            if i < len(lines):
                url_line = lines[i]
                if name_match and not url_line.startswith('#'):
                    name = name_match.group(1).strip()
                    group = group_match.group(1) if group_match else ""
                    
                    raw_clean = re.sub(r'\[.*$', '', name).strip()
                    clean = clean_channel_name(raw_clean)
                    
                    target_url = url_line.strip()
                    
                    # 1. Try YouTube Live first if applicable
                    is_yt_success = False
                    if name in YOUTUBE_CHANNELS:
                        print(f"Checking YouTube live for {name}...")
                        yt_m3u8 = extract_youtube_m3u8(YOUTUBE_CHANNELS[name])
                        if yt_m3u8:
                            target_url = yt_m3u8
                            print(f" -> Success! Using YouTube stream.")
                            is_yt_success = True
                        else:
                            print(f" -> Not live. Falling back to targeted iptv-org.")
                    
                    # 2. Fallback to targeted iptv-org if youtube fails or isn't applicable
                    if not is_yt_success:
                        primary_data = None
                        if "Nepali" in group:
                            primary_data = nepali_data
                        elif "Indian" in group or "Kids" in group or "Movies" in group:
                            primary_data = indian_data
                        elif "News" in group or "International" in group:
                            primary_data = english_data
                            
                        best_match_url = None
                        if primary_data and clean in primary_data:
                            best_match_url = primary_data[clean]
                        if not best_match_url and primary_data:
                            for k, v in primary_data.items():
                                if len(clean) > 3 and len(k) > 3:
                                    if k == clean or k.startswith(clean + " ") or clean.startswith(k + " "):
                                        best_match_url = v
                                        break
                        if not best_match_url and clean in global_data:
                            best_match_url = global_data[clean]
                            
                        if best_match_url:
                            target_url = best_match_url
                    
                    new_lines.append(target_url + '\n')
                else:
                    new_lines.append(url_line)
        else:
            new_lines.append(line)
        i += 1
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    process_m3u("playlist_working.m3u8")
