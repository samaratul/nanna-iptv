import urllib.request
import re
import urllib.parse
import time

def get_logo(name):
    query = urllib.parse.quote(name + " logo png")
    url = f"https://html.duckduckgo.com/html/?q={query}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        time.sleep(0.5) # Prevent rate limiting
        html = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'//external-content.duckduckgo.com/iu/\?u=([^&]+)', html)
        if match:
            return urllib.parse.unquote(match.group(1))
    except Exception as e:
        print(f"Failed for {name}: {e}")
    return ""

def process_m3u(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.startswith('#EXTINF:') and 'tvg-logo=' not in line:
            name_match = re.search(r',(.*)$', line)
            if name_match:
                name = name_match.group(1).strip()
                print(f"Searching logo for {name}...")
                logo = get_logo(name)
                if logo:
                    line = line.replace('group-title', f'tvg-logo="{logo}" group-title')
                    print(f" -> Found: {logo}")
                else:
                    print(f" -> Not found")
        new_lines.append(line)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    process_m3u("playlist_working.m3u8")
