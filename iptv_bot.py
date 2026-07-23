import urllib.request
import re
import os

# Configuration
IPTV_ORG_URL = "https://iptv-org.github.io/iptv/index.m3u"
BASE_PLAYLIST = "base_playlist.m3u8"
OUTPUT_PLAYLIST = "master_playlist.m3u8"

def normalize_name(name):
    # Remove special characters, lowercase, and strip spaces for better matching
    return re.sub(r'[^a-zA-Z0-9]', '', name).lower()

def fetch_global_playlist():
    print(f"Fetching global playlist from {IPTV_ORG_URL}...")
    req = urllib.request.Request(IPTV_ORG_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            return content
    except Exception as e:
        print(f"Error fetching global playlist: {e}")
        return ""

def parse_m3u(content):
    channels = {}
    lines = content.split('\n')
    current_name = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            # Extract the channel name (everything after the last comma)
            parts = line.split(',')
            if len(parts) > 1:
                current_name = parts[-1].strip()
        elif line.startswith("http") and current_name:
            norm_name = normalize_name(current_name)
            # Only save the first working link we find for a channel
            if norm_name not in channels:
                channels[norm_name] = line
            current_name = None
            
    print(f"Parsed {len(channels)} unique channels from iptv-org.")
    return channels

def generate_master_playlist(global_channels):
    if not os.path.exists(BASE_PLAYLIST):
        print(f"Error: {BASE_PLAYLIST} not found!")
        return

    print(f"Reading {BASE_PLAYLIST}...")
    with open(BASE_PLAYLIST, 'r', encoding='utf-8') as f:
        base_lines = f.readlines()

    output_lines = []
    current_channel_name = None
    found_count = 0
    total_count = 0

    for line in base_lines:
        clean_line = line.strip()
        if clean_line.startswith("#EXTINF"):
            output_lines.append(line)
            parts = clean_line.split(',')
            if len(parts) > 1:
                current_channel_name = parts[-1].strip()
                total_count += 1
        elif clean_line.startswith("http") and "placeholder-stream-url" in clean_line:
            if current_channel_name:
                norm_name = normalize_name(current_channel_name)
                # Try exact match first
                if norm_name in global_channels:
                    print(f"[SUCCESS] Found working link for: {current_channel_name}")
                    output_lines.append(global_channels[norm_name] + "\n")
                    found_count += 1
                else:
                    # Fallback: Check if the channel name is a substring of any global channel
                    # e.g. "Kantipur TV" matching "Kantipur TV HD"
                    fallback_link = None
                    for glob_name, glob_link in global_channels.items():
                        if norm_name in glob_name or glob_name in norm_name:
                            if len(norm_name) > 4: # Don't match super short acronyms loosely
                                fallback_link = glob_link
                                break
                    
                    if fallback_link:
                        print(f"[SUCCESS] Found fallback link for: {current_channel_name}")
                        output_lines.append(fallback_link + "\n")
                        found_count += 1
                    else:
                        print(f"[MISSING] Could not find link for: {current_channel_name}")
                        output_lines.append(line) # keep placeholder
            else:
                output_lines.append(line)
            current_channel_name = None
        else:
            output_lines.append(line)

    print(f"Writing updated playlist to {OUTPUT_PLAYLIST}...")
    with open(OUTPUT_PLAYLIST, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
        
    print(f"Done! Successfully updated {found_count} out of {total_count} channels.")

if __name__ == "__main__":
    global_content = fetch_global_playlist()
    if global_content:
        global_channels = parse_m3u(global_content)
        generate_master_playlist(global_channels)
