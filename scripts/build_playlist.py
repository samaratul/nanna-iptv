import urllib.request
import re
import os

# Path to the artifact markdown file containing the master list
channel_list_file = r"C:\Users\Atul Upadhyaya\.gemini\antigravity\brain\b0b23995-48d6-40ab-b0c8-a537e6cd8d07\channel_list.md"

master_channels = []
current_lang = "Global"

# 1. Parse Master List
with open(channel_list_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("## "):
            match = re.match(r"## ([^\(]+)", line)
            if match:
                current_lang = match.group(1).strip()
        elif line.startswith("- "):
            raw_name = line[2:].strip()
            name_clean = re.sub(r"\(.*?\)", "", raw_name).strip()
            name_clean = re.sub(r"\[.*?\]", "", name_clean).strip()
            
            master_channels.append({
                "original_name": raw_name,
                "search_name": name_clean,
                "language": current_lang,
                "genre": "General",
                "active": False,
                "url": "http://inactive.local/stream.m3u8",
                "logo": ""
            })

hardcoded_streams = {
    "Kantipur TV HD": "https://ktvhdsg.ekantipur.com:8443/high_quality_85840165/hd/playlist.m3u8",
    "AP1 TV HD": "http://maxotts.maxdigitaltv.com/x-media/C22/master.m3u8",
    "News 24 HD": "http://maxotts.maxdigitaltv.com/x-media/C9/master.m3u8",
    "Capital TV HD": "https://streaming.tvnepal.com:19360/capitaltv/capitaltv.m3u8",
    "City One Television": "http://maxotts.maxdigitaltv.com/x-media/C209/master.m3u8",
    "METV HD": "http://maxotts.maxdigitaltv.com/x-media/C168/master.m3u8",
    "Nepal 1": "https://d1msejlow1t3l4.cloudfront.net/fta/nepal1/chunks.m3u8",
    "Mithila Nepal TV HD": "http://150.107.205.212:1935/live/mithila/playlist.m3u8",
    "Dhaulagiri Television": "http://maxotts.maxdigitaltv.com/x-media/C117/master.m3u8"
}

sources = [
    "https://iptv-org.github.io/iptv/countries/in.m3u",
    "https://iptv-org.github.io/iptv/countries/np.m3u",
    "https://iptv-org.github.io/iptv/countries/us.m3u",
    "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "https://iptv-org.github.io/iptv/categories/news.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "https://iptv-org.github.io/iptv/categories/movies.m3u",
    "https://iptv-org.github.io/iptv/categories/kids.m3u",
    "https://iptv-org.github.io/iptv/categories/music.m3u",
    "https://iptv-org.github.io/iptv/categories/documentary.m3u"
]

ALLOWED_LANGS = ["Nepali", "Hindi", "English", "Bhojpuri"]

def get_best_language(name, orig_cat, iptv_lang):
    if iptv_lang:
        for l in iptv_lang.split(';'):
            if l in ALLOWED_LANGS: return l
    if orig_cat in ALLOWED_LANGS: return orig_cat
    
    n = name.lower()
    if any(x in n for x in ["nepal", "kantipur", "ap1", "ntv", "himalaya", "image", "avenues", "sagarmatha"]): return "Nepali"
    if any(x in n for x in ["bhojpuri", "biskope", "mahuwa", "ganga", "anjan"]): return "Bhojpuri"
    if any(x in n for x in ["bbc", "cnn", "sky", "fox", "hbo", "movies now", "axn", "english", "discovery", "nat geo", "tlc", "history", "cbs", "bloomberg", "cnbc", "mtv"]): return "English"
    return "Hindi"

def get_best_genre(orig_cat, iptv_group):
    if orig_cat not in ALLOWED_LANGS and orig_cat != "Global":
        return orig_cat
    if iptv_group and iptv_group != "General":
        return iptv_group
    return "General"

# 2. Search for active links
for source in sources:
    try:
        print(f"Fetching {source}...")
        req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
        content = urllib.request.urlopen(req).read().decode('utf-8')
        lines = content.split('\n')
        
        current_logo = ""
        current_name = ""
        current_group = ""
        current_iptv_lang = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF'):
                logo_match = re.search(r'tvg-logo="([^"]+)"', line)
                if logo_match: current_logo = logo_match.group(1)
                
                group_match = re.search(r'group-title="([^"]+)"', line)
                if group_match: current_group = group_match.group(1)
                
                lang_match = re.search(r'tvg-language="([^"]+)"', line)
                if lang_match: current_iptv_lang = lang_match.group(1)
                
                parts = line.split(',')
                if len(parts) > 1:
                    current_name = parts[-1].strip()
            elif line.startswith('http') and current_name:
                for ch in master_channels:
                    if not ch["active"]:
                        if ch["search_name"].lower() == current_name.lower() or ch["search_name"].lower() in current_name.lower():
                            ch["active"] = True
                            ch["url"] = line
                            ch["genre"] = get_best_genre(ch["language"], current_group)
                            ch["language"] = get_best_language(ch["search_name"], ch["language"], current_iptv_lang)
                            if current_logo:
                                ch["logo"] = current_logo
                current_name = ""
                current_logo = ""
                current_group = ""
                current_iptv_lang = ""
    except Exception as e:
        print(f"Error fetching {source}: {e}")

# Apply hardcoded streams and cleanup inactive channels
for ch in master_channels:
    for hc_name, hc_url in hardcoded_streams.items():
        if hc_name.lower() in ch["search_name"].lower() or hc_name.lower() in ch["original_name"].lower():
            ch["active"] = True
            ch["url"] = hc_url
    
    if not ch["active"]:
        ch["genre"] = get_best_genre(ch["language"], "")
        ch["language"] = get_best_language(ch["search_name"], ch["language"], "")

active_count = sum(1 for ch in master_channels if ch["active"])
inactive_count = len(master_channels) - active_count

with open("../playlist.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for ch in master_channels:
        status = "active" if ch["active"] else "inactive"
        logo_tag = f' tvg-logo="{ch["logo"]}"' if ch["logo"] else ''
        f.write(f'#EXTINF:-1 tvg-language="{ch["language"]}" tvg-status="{status}"{logo_tag} group-title="{ch["genre"]}",{ch["search_name"]}\n')
        f.write(f'{ch["url"]}\n\n')

print(f"Master playlist generated! Total: {len(master_channels)} | Active: {active_count} | Inactive: {inactive_count}")
