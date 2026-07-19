import urllib.request
import re

def clean_channel_name(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\[.*?\]', '', name)
    name = name.lower().replace(' hd', '').replace(' tv', '').replace(' channel', '').strip()
    name = re.sub(r'\s+', ' ', name)
    return name

def get_iptv_org_logos():
    print("Downloading iptv-org index.m3u...")
    url = "https://iptv-org.github.io/iptv/index.m3u"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req).read().decode('utf-8')
    lines = data.split('\n')
    
    logos = {}
    for line in lines:
        if line.startswith('#EXTINF:'):
            name_match = re.search(r',(.*)$', line)
            logo_match = re.search(r'tvg-logo="([^"]+)"', line)
            if name_match and logo_match:
                name = name_match.group(1).strip()
                logo = logo_match.group(1).strip()
                if logo:
                    logos[clean_channel_name(name)] = logo
    return logos

def process_m3u(file_path, iptv_logos):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    found_count = 0
    for line in lines:
        if line.startswith('#EXTINF:'):
            name_match = re.search(r',(.*)$', line)
            if name_match:
                name = name_match.group(1).strip()
                raw_clean = re.sub(r'\[.*$', '', name).strip()
                clean = clean_channel_name(raw_clean)
                
                best_match = None
                if clean in iptv_logos:
                    best_match = iptv_logos[clean]
                else:
                    # Avoid matching too broadly by checking word boundaries
                    for k, v in iptv_logos.items():
                        if len(clean) > 3 and len(k) > 3:
                            if k == clean or k.startswith(clean + " ") or clean.startswith(k + " "):
                                best_match = v
                                break
                            
                if best_match:
                    line = re.sub(r' tvg-logo="[^"]*"', '', line)
                    line = line.replace('group-title', f'tvg-logo="{best_match}" group-title')
                    print(f"Matched {name} -> {best_match}")
                    found_count += 1
                else:
                    print(f"Not matched: {name} (clean: {clean})")
        new_lines.append(line)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Updated {found_count} channels with iptv-org logos.")

if __name__ == "__main__":
    logos = get_iptv_org_logos()
    print(f"Loaded {len(logos)} logos from iptv-org")
    process_m3u("playlist_working.m3u8", logos)
