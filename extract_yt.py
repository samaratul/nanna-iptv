import yt_dlp

urls = {
    'Aaj Tak': 'https://www.youtube.com/@aajtak/live',
    'News24 Nepal': 'https://www.youtube.com/@news24tvchannel/live',
    'NDTV 24x7': 'https://www.youtube.com/@NDTV/live',
    'ABP News': 'https://www.youtube.com/@abpnews/live',
    'Al Jazeera': 'https://www.youtube.com/@aljazeeraenglish/live'
}

ydl_opts = {'format': 'best', 'quiet': True, 'simulate': True, 'forceurl': True, 'nocheckcertificate': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for name, url in urls.items():
        try:
            info = ydl.extract_info(url, download=False)
            print(f"{name}:\n{info['url']}\n")
        except Exception as e:
            print(f"{name}: NOT LIVE or ERROR\n")
