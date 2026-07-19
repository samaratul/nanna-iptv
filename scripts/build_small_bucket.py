import os
import json

# Use paths relative to this script so it works from anywhere
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)

targets_file = os.path.join(script_dir, 'curation_targets.json')
input_file = os.path.join(root_dir, 'bucket_public_working.m3u8')
output_file = os.path.join(root_dir, 'playlist_working.m3u8')

with open(targets_file, 'r', encoding='utf-8') as f:
    targets = json.load(f)

# Structure to hold final selected channels:
# final_buckets[lang][genre] = { 'Channel Name': { 'url': ..., 'is_hd': ... } }
final_buckets = {}
for lang in targets:
    final_buckets[lang] = {}
    for genre in targets[lang]:
        final_buckets[lang][genre] = {}

if os.path.exists(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
else:
    print(f"{input_file} not found.")
    lines = []

current_extinf = ""
current_name = ""

for line in lines:
    line = line.strip()
    if line.startswith('#EXTINF'):
        current_extinf = line
        current_name = line.split(',')[-1].strip()
    elif line.startswith('http') and current_extinf:
        url = line
        name_lower = current_name.lower()
        
        # 1. Completely ban 576p streams
        if "576" in name_lower:
            current_extinf = ""
            continue
            
        # 2. Check if it matches any target
        is_hd = "hd" in name_lower or "1080" in name_lower or "720" in name_lower
        
        matched = False
        for lang, genres in targets.items():
            for genre, target_list in genres.items():
                for target in target_list:
                    if target.lower() in name_lower:
                        # Found a match!
                        # We deduplicate by the exact TARGET name from JSON.
                        # If we already have a stream for this target, only replace it if this one is HD and the old one isn't.
                        existing = final_buckets[lang][genre].get(target)
                        if not existing or (is_hd and not existing['is_hd']):
                            # Rewrite the EXTINF name to perfectly match the requested target string
                            import re
                            new_extinf = current_extinf
                            # Replace the channel name (everything after the last comma) with the target
                            new_extinf = re.sub(r',(.*)$', f',{target}', new_extinf)
                            
                            final_buckets[lang][genre][target] = {
                                'extinf': new_extinf,
                                'url': url,
                                'is_hd': is_hd
                            }
                        matched = True
                        break # stop checking targets in this genre
                if matched:
                    break
            if matched:
                break
                
        current_extinf = ""

# Now write the curated playlist
with open(output_file, 'w', encoding='utf-8') as out:
    out.write('#EXTM3U\n')
    
    total_added = 0
    
    for lang in targets:
        for genre in targets[lang]:
            channels = final_buckets[lang][genre]
            if not channels:
                continue
                
            out.write('\n# ======================\n')
            out.write(f'# {lang} - {genre}\n')
            out.write('# ======================\n')
            
            # Sort by name, HD first
            sorted_channels = sorted(channels.items(), key=lambda x: (not x[1]['is_hd'], x[0]))
            
            for name, data in sorted_channels:
                # Rewrite the group-title so it is uniform
                # We can replace the existing group-title with our curated one
                import re
                extinf = data['extinf']
                extinf = re.sub(r'group-title=".*?"', f'group-title="{lang} - {genre}"', extinf)
                if 'group-title' not in extinf:
                    extinf = extinf.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{lang} - {genre}"')
                
                out.write(f'{extinf}\n')
                out.write(f"{data['url']}\n")
                total_added += 1

print(f"Successfully generated curated {total_added}-channel 'playlist_working.m3u8' using strict target whitelist.")
