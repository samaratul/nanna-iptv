import urllib.request
import re

try:
    html = urllib.request.urlopen('https://live.ntv.org.np/main.f76c872c990e7563b35e.js').read().decode('utf-8')
    m3u8_links = set(re.findall(r'https?://[^\s"\'<>]+', html))
    api_links = [l for l in m3u8_links if 'api' in l or 'stream' in l or 'live' in l]
    print("Found M3U8 links:")
    for link in m3u8_links:
        print(link)
except Exception as e:
    print(f"Error: {e}")
