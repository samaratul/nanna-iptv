import urllib.request
import re

URLS = [
    "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8",
    "https://romaxa55.github.io/world_ip_tv/output/index.m3u",
    "https://iptv-org.github.io/iptv/index.language.m3u",
    "https://iptv-org.github.io/iptv/index.m3u"
]

LOCAL_FILES = [
    "extracted_channels.m3u",
    "playlist.m3u8"
]

def classify_language(name, iptv_lang, group_title):
    n = name.lower()
    
    # Check strict keywords
    if any(x in n for x in ["nepal", "kantipur", "ap1", "ntv", "himalaya", "image", "avenues", "sagarmatha", "capital", "dhaulagiri", "mithila", "yo ho", "news 24"]): return "Nepali"
    if any(x in n for x in ["bhojpuri", "biskope", "mahuwa", "ganga", "anjan", "sangeet bhojpuri"]): return "Bhojpuri"
    
    # Check language tag
    if iptv_lang:
        langs = iptv_lang.lower().split(';')
        for l in langs:
            if "hin" in l or "hindi" in l: return "Hindi"
            if "eng" in l or "english" in l: return "English"
            if "nep" in l or "nepali" in l: return "Nepali"
            if "bho" in l or "bhojpuri" in l: return "Bhojpuri"
            
    # Check group title for embedded language
    if group_title:
        gt = group_title.lower()
        if "hindi" in gt: return "Hindi"
        if "english" in gt: return "English"
        if "nepali" in gt: return "Nepali"
        if "bhojpuri" in gt: return "Bhojpuri"

    # Fallback to English/Hindi for popular channels
    if any(x in n for x in ["aaj tak", "dd ", "india", "samachar", "khabar", "bharat", "zee", "star", "sony", "colors", "dangal", "b4u", "shemaroo", "abp", "republic", "ndtv", "manoranjan", "sansad", "9x", "goldmines", "maha", "shubh", "aastha", "jinvani", "ishwar"]): return "Hindi"
    if any(x in n for x in ["bbc", "cnn", "sky", "fox", "hbo", "movies now", "axn", "english", "discovery", "nat geo", "tlc", "history", "cbs", "bloomberg", "cnbc", "mtv", "wion", "arirang", "cgtn"]): return "English"

    return None

def classify_genre(name, iptv_group):
    n = name.lower()
    if any(x in n for x in ["movie", "cinema", "film", "plex", "goldmines"]): return "Movies"
    if any(x in n for x in ["news", "samachar", "khabar", "24", "tak", "bharat", "bbc", "cnn", "ndtv"]): return "News"
    if any(x in n for x in ["music", "mtv", "jalwa", "zing", "vh1"]): return "Music"
    if any(x in n for x in ["sport", "ten", "golf", "nba", "nfl", "mlb"]): return "Sports"
    if any(x in n for x in ["bhakti", "darshan", "aastha", "angel", "peace", "god", "tbn", "islam", "quran"]): return "Devotional"
    if any(x in n for x in ["earth", "discovery", "history", "geo", "tlc", "travel", "lifestyle", "fashion", "animal"]): return "Lifestyle"
    
    if iptv_group:
        g = iptv_group.lower()
        if "movie" in g: return "Movies"
        if "news" in g: return "News"
        if "music" in g: return "Music"
        if "sport" in g: return "Sports"
        if "reli" in g or "spirit" in g or "devotion" in g: return "Devotional"
        if "life" in g or "docu" in g or "educat" in g: return "Lifestyle"
        if "entert" in g or "general" in g or "kid" in g: return "Entertainment"

    return "Entertainment"

unique_urls = set()
output_channels = []

def parse_m3u_lines(lines, source_name):
    global unique_urls, output_channels
    current_extinf = ""
    current_name = ""
    current_group = ""
    current_lang = ""
    current_logo = ""
    
    added = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#EXTINF'):
            current_extinf = line
            # Parse attributes
            name_parts = line.split(',')
            current_name = name_parts[-1].strip() if len(name_parts) > 1 else ""
            
            grp = re.search(r'group-title="([^"]+)"', line)
            current_group = grp.group(1) if grp else ""
            
            lng = re.search(r'tvg-language="([^"]+)"', line)
            current_lang = lng.group(1) if lng else ""
            
            lgo = re.search(r'tvg-logo="([^"]+)"', line)
            current_logo = lgo.group(1) if lgo else ""
            
        elif line.startswith('http') and current_extinf:
            url = line
            if url not in unique_urls:
                lang = classify_language(current_name, current_lang, current_group)
                if lang: # Only accept our 4 target languages
                    genre = classify_genre(current_name, current_group)
                    
                    unique_urls.add(url)
                    output_channels.append({
                        "name": current_name,
                        "url": url,
                        "logo": current_logo,
                        "language": lang,
                        "genre": genre
                    })
                    added += 1
            current_extinf = ""
    print(f"Added {added} unique targeted channels from {source_name}")

# 1. Parse Remote URLs
for url in URLS:
    try:
        print(f"Fetching {url}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        content = urllib.request.urlopen(req).read().decode('utf-8')
        parse_m3u_lines(content.split('\n'), url)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

# 2. Parse Local Files
import os
for local_file in LOCAL_FILES:
    if os.path.exists(local_file):
        print(f"Reading local {local_file}...")
        with open(local_file, "r", encoding="utf-8") as f:
            parse_m3u_lines(f.readlines(), local_file)

# Write Master Public Bucket
with open("bucket_public.m3u8", "w", encoding="utf-8") as out:
    out.write("#EXTM3U\n")
    for ch in output_channels:
        logo_str = f' tvg-logo="{ch["logo"]}"' if ch["logo"] else ''
        out.write(f'#EXTINF:-1 tvg-language="{ch["language"]}"{logo_str} group-title="{ch["language"]} - {ch["genre"]}",{ch["name"]}\n')
        out.write(f'{ch["url"]}\n')

print(f"\nSuccessfully built Large Bucket 'bucket_public.m3u8' with {len(output_channels)} streams.")
