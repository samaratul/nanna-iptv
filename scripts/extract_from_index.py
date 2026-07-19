import urllib.request
import re

url = "https://iptv-org.github.io/iptv/index.m3u"
print(f"Downloading {url}...")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    content = urllib.request.urlopen(req).read().decode('utf-8')
    lines = content.split('\n')
    print(f"Total lines in index.m3u: {len(lines)}")
except Exception as e:
    print(f"Error fetching: {e}")
    exit(1)

def is_target_language(name, iptv_lang, group_title):
    n = name.lower()
    
    # Check iptv-org language tag
    if iptv_lang:
        langs = iptv_lang.lower().split(';')
        for l in langs:
            if "hin" in l or "hindi" in l: return True
            if "nep" in l or "nepali" in l: return True
            if "bho" in l or "bhojpuri" in l: return True

    # Check strong name keywords
    if any(x in n for x in ["nepal", "kantipur", "ap1", "ntv", "himalaya", "image", "avenues", "sagarmatha", "capital", "dhaulagiri", "mithila", "yo ho", "news 24"]): return True
    if any(x in n for x in ["bhojpuri", "biskope", "mahuwa", "ganga", "anjan", "sangeet bhojpuri"]): return True
    if any(x in n for x in ["aaj tak", "dd ", "india", "samachar", "khabar", "bharat", "zee", "star", "sony", "colors", "dangal", "b4u", "shemaroo", "abp", "republic", "ndtv", "manoranjan", "sansad", "9x", "goldmines", "maha", "shubh", "aastha", "jinvani", "ishwar"]): return True
    
    return False

extracted_lines = ["#EXTM3U\n"]
current_extinf = ""
count = 0

for line in lines:
    line = line.strip()
    if line.startswith('#EXTINF'):
        current_extinf = line
    elif line.startswith('http') and current_extinf:
        # Extract attributes to test
        name_match = current_extinf.split(',')
        name = name_match[-1].strip() if len(name_match) > 1 else ""
        
        lang_match = re.search(r'tvg-language="([^"]+)"', current_extinf)
        iptv_lang = lang_match.group(1) if lang_match else ""
        
        group_match = re.search(r'group-title="([^"]+)"', current_extinf)
        group_title = group_match.group(1) if group_match else ""
        
        if is_target_language(name, iptv_lang, group_title):
            extracted_lines.append(current_extinf + "\n")
            extracted_lines.append(line + "\n")
            count += 1
            
        current_extinf = ""

output_file = "extracted_channels.m3u"
with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(extracted_lines)

print(f"Successfully extracted {count} Nepali, Bhojpuri, and Hindi channels to {output_file}.")
