import urllib.request
import re
try:
    html = urllib.request.urlopen('https://live.ntv.org.np/main.f76c872c990e7563b35e.js').read().decode('utf-8')
    links = set(re.findall(r'https?://[^\s"\'<>]+', html))
    print("Found HTTP links in JS:")
    for link in links:
        if 'ntv' in link or 'api' in link or 'live' in link or 'video' in link:
            print(link)
except Exception as e:
    print(f"Error: {e}")
