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
            # Extract category name, ignoring the (XX channels) part
            match = re.match(r"## ([^\(]+)", line)
            if match:
                current_lang = match.group(1).strip()
        elif line.startswith("- "):
            # Extract channel name, ignoring (1080p) or [Not 24/7]
            raw_name = line[2:].strip()
            name_clean = re.sub(r"\(.*?\)", "", raw_name).strip()
            name_clean = re.sub(r"\[.*?\]", "", name_clean).strip()
            
            master_channels.append({
                "original_name": raw_name,
                "search_name": name_clean,
                "language": current_lang,
                "genre": "General", # Default genre since the list doesn't specify deep subcategories
                "active": False,
                "url": "http://inactive.local/stream.m3u8",
                "logo": ""
            })

# Hardcoded fallback for some specific channels to ensure they always work
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

# 2. Search for active links
for source in sources:
    try:
        print(f"Fetching {source}...")
        req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
        content = urllib.request.urlopen(req).read().decode('utf-8')
        lines = content.split('\n')
        
        current_logo = ""
        current_name = ""
        current_group = "General"
        
        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF'):
                logo_match = re.search(r'tvg-logo="([^"]+)"', line)
                if logo_match:
                    current_logo = logo_match.group(1)
                
                group_match = re.search(r'group-title="([^"]+)"', line)
                if group_match:
                    current_group = group_match.group(1)
                
                parts = line.split(',')
                if len(parts) > 1:
                    current_name = parts[-1].strip()
            elif line.startswith('http') and current_name:
                # Check if this channel matches any in our master list that isn't active yet
                for ch in master_channels:
                    if not ch["active"]:
                        # Exact match or very close substring match
                        if ch["search_name"].lower() == current_name.lower() or ch["search_name"].lower() in current_name.lower():
                            ch["active"] = True
                            ch["url"] = line
                            ch["genre"] = current_group if current_group else "General"
                            if current_logo:
                                ch["logo"] = current_logo
                current_name = ""
                current_logo = ""
                current_group = "General"
    except Exception as e:
        print(f"Error fetching {source}: {e}")

# Apply hardcoded streams
for ch in master_channels:
    for hc_name, hc_url in hardcoded_streams.items():
        if hc_name.lower() in ch["search_name"].lower() or hc_name.lower() in ch["original_name"].lower():
            ch["active"] = True
            ch["url"] = hc_url

# 3. Write to M3U
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
