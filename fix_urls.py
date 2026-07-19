import urllib.request
import re

def clean_channel_name(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\[.*?\]', '', name)
    name = name.lower().replace(' hd', '').replace(' tv', '').replace(' channel', '').strip()
    name = re.sub(r'\s+', ' ', name)
    return name

def get_iptv_org_data():
    print("Downloading iptv-org index.m3u to fetch correct stream URLs...")
    url = "https://iptv-org.github.io/iptv/index.m3u"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
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
            # It's a URL
            clean = clean_channel_name(current_name)
            # Just take the first working URL we find for a channel name
            if clean not in channels_data:
                channels_data[clean] = line
            current_name = None
            
    return channels_data

def process_m3u(file_path, iptv_data):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    found_count = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('#EXTINF:'):
            name_match = re.search(r',(.*)$', line)
            new_lines.append(line)
            
            # Next line should be URL
            i += 1
            if i < len(lines):
                url_line = lines[i]
                if name_match and not url_line.startswith('#'):
                    name = name_match.group(1).strip()
                    raw_clean = re.sub(r'\[.*$', '', name).strip()
                    clean = clean_channel_name(raw_clean)
                    
                    best_match_url = None
                    if clean in iptv_data:
                        best_match_url = iptv_data[clean]
                    else:
                        for k, v in iptv_data.items():
                            if len(clean) > 3 and len(k) > 3:
                                if k == clean or k.startswith(clean + " ") or clean.startswith(k + " "):
                                    best_match_url = v
                                    break
                    
                    if best_match_url:
                        new_lines.append(best_match_url + '\n')
                        if best_match_url.strip() != url_line.strip():
                            print(f"Fixed URL for {name}")
                            found_count += 1
                    else:
                        # Keep original if no match
                        new_lines.append(url_line)
                else:
                    new_lines.append(url_line)
        else:
            new_lines.append(line)
        i += 1
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"\nFixed {found_count} broken/mismapped stream URLs using iptv-org.")

if __name__ == "__main__":
    iptv_data = get_iptv_org_data()
    print(f"Loaded {len(iptv_data)} channel URLs from iptv-org")
    process_m3u("playlist_working.m3u8", iptv_data)
