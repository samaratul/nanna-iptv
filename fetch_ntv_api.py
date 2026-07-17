import urllib.request
import re

try:
    html = urllib.request.urlopen('https://live.ntv.org.np/main.f76c872c990e7563b35e.js').read().decode('utf-8')
    api_paths = set(re.findall(r'[\'"]/api/[^\'"]+[\'"]', html))
    print("API paths:")
    for path in api_paths:
        print(path)
except Exception as e:
    print(f"Error: {e}")
