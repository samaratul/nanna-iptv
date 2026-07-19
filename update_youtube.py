import os
import re
import urllib.request
import yt_dlp

YOUTUBE_CHANNELS = {
    'Aaj Tak': 'https://www.youtube.com/@aajtak/live',
    'NDTV 24x7': 'https://www.youtube.com/@NDTV/live',
    'ABP News': 'https://www.youtube.com/@abpnews/live',
    'Al Jazeera HD': 'https://www.youtube.com/@aljazeeraenglish/live',
    'India Today': 'https://www.youtube.com/@indiatoday/live',
    'Kantipur HD': 'https://www.youtube.com/@kantipurtvhd/live',
    'News 24': 'https://www.youtube.com/@news24tvchannel/live'
}

def clean_channel_name(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\[.*?\]', '', name)
    name = name.lower().replace(' hd', '').replace(' tv', '').replace(' channel', '').strip()
    name = re.sub(r'\s+', ' ', name)
    return name

def get_iptv_org_data():
    print("Fetching iptv-org fallback URLs...")
    url = "https://iptv-org.github.io/iptv/index.m3u"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = urllib.request.urlopen(req).read().decode('utf-8')
        lines = data.split('\n')
        
        channels_data = {}
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
                if clean not in channels_data:
                    channels_data[clean] = line
                current_name = None
        return channels_data
    except Exception as e:
        print(f"Failed to fetch iptv-org data: {e}")
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
    iptv_data = get_iptv_org_data()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('#EXTINF:'):
            name_match = re.search(r',(.*)$', line)
            new_lines.append(line)
            
            i += 1
            if i < len(lines):
                url_line = lines[i]
                if name_match and not url_line.startswith('#'):
                    name = name_match.group(1).strip()
                    raw_clean = re.sub(r'\[.*$', '', name).strip()
                    clean = clean_channel_name(raw_clean)
                    
                    target_url = url_line.strip()
                    
                    # 1. Try YouTube Live first
                    if name in YOUTUBE_CHANNELS:
                        print(f"Checking YouTube live for {name}...")
                        yt_m3u8 = extract_youtube_m3u8(YOUTUBE_CHANNELS[name])
                        if yt_m3u8:
                            target_url = yt_m3u8
                            print(f" -> Success! Using YouTube stream.")
                        else:
                            print(f" -> Not live. Falling back to iptv-org.")
                            # Fallback to iptv-org
                            if clean in iptv_data:
                                target_url = iptv_data[clean]
                            else:
                                for k, v in iptv_data.items():
                                    if len(clean) > 3 and len(k) > 3:
                                        if k == clean or k.startswith(clean + " ") or clean.startswith(k + " "):
                                            target_url = v
                                            break
                    
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
