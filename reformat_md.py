import re

lines = open('playlist_working.m3u8', encoding='utf-8').readlines()
out = open('final_verified_channels_categorized.md', 'w', encoding='utf-8')
out.write('# Verified Whitelisted Channel Lineup\n\n')

data = {}

for line in lines:
    if line.startswith('# ======================'):
        continue
    elif line.startswith('#EXTINF'):
        match = re.search(r'group-title="(.*?)"', line)
        if match:
            group = match.group(1)
            if ' - ' in group:
                lang, genre = group.split(' - ', 1)
            else:
                lang = group
                genre = 'Unknown'
                
            if lang not in data:
                data[lang] = {}
            if genre not in data[lang]:
                data[lang][genre] = []
            name = line.split(',')[-1].strip()
            data[lang][genre].append(name)

for lang in data:
    out.write(f'## {lang} (Main Category)\n')
    for genre in data[lang]:
        out.write(f'### {genre} (Sub Category)\n')
        for name in data[lang][genre]:
            out.write(f'- {name}\n')
    out.write('\n')

out.close()
