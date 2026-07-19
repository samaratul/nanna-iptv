import urllib.request
import re
import os

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

def process_m3u(file_path):
    # Fetch specific databases to avoid cross-country collisions
    nepali_data = fetch_m3u_dict("https://iptv-org.github.io/iptv/countries/np.m3u")
    indian_data = fetch_m3u_dict("https://iptv-org.github.io/iptv/countries/in.m3u")
    english_data = fetch_m3u_dict("https://iptv-org.github.io/iptv/languages/eng.m3u")
    
    # Also fetch full index as last resort
    global_data = fetch_m3u_dict("https://iptv-org.github.io/iptv/index.m3u")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    fixed_count = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        if line.startswith('#EXTINF:'):
            # parse name and group-title
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
                    
                    # Choose data source based on group
                    primary_data = None
                    if "Nepali" in group:
                        primary_data = nepali_data
                    elif "Indian" in group or "Kids" in group or "Movies" in group:
                        primary_data = indian_data
                    elif "News" in group or "International" in group:
                        primary_data = english_data
                    
                    best_match_url = None
                    
                    # 1. Try primary specific data
                    if primary_data and clean in primary_data:
                        best_match_url = primary_data[clean]
                        
                    # 2. If not found, try fuzzy in primary
                    if not best_match_url and primary_data:
                        for k, v in primary_data.items():
                            if len(clean) > 3 and len(k) > 3:
                                if k == clean or k.startswith(clean + " ") or clean.startswith(k + " "):
                                    best_match_url = v
                                    break
                                    
                    # 3. If still not found, try global data (exact only)
                    if not best_match_url and clean in global_data:
                        best_match_url = global_data[clean]
                    
                    if best_match_url:
                        new_lines.append(best_match_url + '\n')
                        if best_match_url.strip() != url_line.strip() and "manifest.googlevideo.com" not in url_line: # ignore youtube links
                            print(f"[{group}] Re-mapped {name} securely to {best_match_url}")
                            fixed_count += 1
                    else:
                        new_lines.append(url_line)
                else:
                    new_lines.append(url_line)
        else:
            new_lines.append(line)
        i += 1
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"\nFixed {fixed_count} mismatched channel URLs using targeted geographic repos.")

if __name__ == "__main__":
    process_m3u("playlist_working.m3u8")
