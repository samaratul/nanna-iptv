from duckduckgo_search import DDGS
import re
import time
import os

def search_logo(query):
    # Clean up broken names like "B4U Bhojpuri [1.2.3" -> "B4U Bhojpuri"
    clean_query = re.sub(r'\[.*$', '', query).strip()
    if not clean_query or clean_query.replace('.', '').isdigit():
        return None
        
    try:
        results = DDGS().images(f"{clean_query} tv channel logo png", max_results=1)
        if results:
            return results[0]['image']
    except Exception as e:
        print(f"Error fetching {clean_query}: {e}")
    return None

def process_m3u(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.startswith('#EXTINF:'):
            name_match = re.search(r',(.*)$', line)
            if name_match:
                name = name_match.group(1).strip()
                # Skip if already has a valid Wikipedia or yt3 logo
                if 'tvg-logo="http' not in line or 'api.dicebear.com' in line:
                    print(f"Searching logo for {name}...")
                    logo = search_logo(name)
                    time.sleep(1.5) # Prevent rate limiting
                    if logo:
                        # Remove existing empty or bad tvg-logo tags if they exist
                        line = re.sub(r' tvg-logo="[^"]*"', '', line)
                        line = line.replace('group-title', f'tvg-logo="{logo}" group-title')
                        print(f" -> Found: {logo}")
                    else:
                        print(f" -> Not found")
        new_lines.append(line)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    process_m3u("playlist_working.m3u8")
