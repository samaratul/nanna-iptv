import re
import os

LOGO_MAP = {
    "Kantipur": "https://upload.wikimedia.org/wikipedia/en/9/9f/Kantipur_Television_Logo.png",
    "AP1 HD": "https://upload.wikimedia.org/wikipedia/commons/3/30/Ap1_TV_logo.png",
    "Himalaya": "https://upload.wikimedia.org/wikipedia/commons/e/ec/Himalaya_Television_Logo.png",
    "News 24": "https://upload.wikimedia.org/wikipedia/commons/8/87/News24_nepal.png",
    "Nepal TV": "https://upload.wikimedia.org/wikipedia/en/9/98/Nepal_Television_Logo.png",
    "NTV News": "https://upload.wikimedia.org/wikipedia/en/9/98/Nepal_Television_Logo.png",
    "Prime TV": "https://upload.wikimedia.org/wikipedia/en/6/6f/Prime_Times_Television_logo.png",
    "Action Sports": "https://upload.wikimedia.org/wikipedia/en/2/23/Action_Sports_Nepal.png",
    "Star Plus": "https://logo.clearbit.com/startv.com",
    "Star Bharat": "https://logo.clearbit.com/startv.com",
    "Star Gold": "https://logo.clearbit.com/startv.com",
    "Star Utsav": "https://logo.clearbit.com/startv.com",
    "Star Sports": "https://logo.clearbit.com/startv.com",
    "Star Movies": "https://logo.clearbit.com/startv.com",
    "Sony Entertainment": "https://logo.clearbit.com/setindia.com",
    "Sony SAB": "https://logo.clearbit.com/sabtv.com",
    "Sony Max": "https://logo.clearbit.com/setindia.com",
    "Sony Ten": "https://logo.clearbit.com/setindia.com",
    "Sony Pix": "https://logo.clearbit.com/sonypictures.com",
    "Zee TV": "https://logo.clearbit.com/zee5.com",
    "Zee Cinema": "https://logo.clearbit.com/zeecinema.com",
    "Zee Cafe": "https://logo.clearbit.com/zee5.com",
    "Zee Anmol": "https://logo.clearbit.com/zee5.com",
    "Zee News": "https://logo.clearbit.com/zeenews.india.com",
    "Colors": "https://logo.clearbit.com/colorstv.com",
    "&TV": "https://logo.clearbit.com/andtv.com",
    "&Pictures": "https://logo.clearbit.com/andtv.com",
    "B4U": "https://logo.clearbit.com/b4utv.com",
    "Aaj Tak": "https://logo.clearbit.com/aajtak.in",
    "News 18": "https://logo.clearbit.com/news18.com",
    "ABP News": "https://logo.clearbit.com/abplive.com",
    "NDTV": "https://logo.clearbit.com/ndtv.com",
    "India Today": "https://logo.clearbit.com/indiatoday.in",
    "BBC": "https://logo.clearbit.com/bbc.com",
    "CNN": "https://logo.clearbit.com/cnn.com",
    "Al Jazeera": "https://logo.clearbit.com/aljazeera.com",
    "TRT": "https://logo.clearbit.com/trtworld.com",
    "France 24": "https://logo.clearbit.com/france24.com",
    "CGTN": "https://logo.clearbit.com/cgtn.com",
    "RT English": "https://logo.clearbit.com/rt.com",
    "ABC": "https://logo.clearbit.com/abc.net.au",
    "WION": "https://logo.clearbit.com/wionews.com",
    "National Geographic": "https://logo.clearbit.com/nationalgeographic.com",
    "Nat Geo": "https://logo.clearbit.com/nationalgeographic.com",
    "Discovery": "https://logo.clearbit.com/discovery.com",
    "Animal Planet": "https://logo.clearbit.com/animalplanet.com",
    "TLC": "https://logo.clearbit.com/tlc.com",
    "History": "https://logo.clearbit.com/historyindia.com",
    "Nickelodeon": "https://logo.clearbit.com/nick.com",
    "Nick Jr": "https://logo.clearbit.com/nickjr.com",
    "Pogo": "https://logo.clearbit.com/pogo.tv",
    "Cartoon Network": "https://logo.clearbit.com/cartoonnetwork.com",
    "Disney": "https://logo.clearbit.com/disney.com",
    "Hungama": "https://logo.clearbit.com/disney.in",
    "Comedy Central": "https://logo.clearbit.com/comedycentral.com",
    "AXN": "https://logo.clearbit.com/axn.com",
    "Romedy Now": "https://logo.clearbit.com/romedy.tv",
    "Goldmines": "https://upload.wikimedia.org/wikipedia/commons/2/23/Goldmines_Telefilms_logo.png"
}

def process_m3u(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.startswith('#EXTINF:'):
            name_match = re.search(r',(.*)$', line)
            if name_match:
                name = name_match.group(1).strip()
                name = re.sub(r'\[.*$', '', name).strip() # clean names like B4U Bhojpuri [1.2.3
                
                # Strip existing tvg-logo tags to reset
                line = re.sub(r' tvg-logo="[^"]*"', '', line)
                
                logo = ""
                for key, val in LOGO_MAP.items():
                    if key in name:
                        logo = val
                        break
                
                if logo:
                    line = line.replace('group-title', f'tvg-logo="{logo}" group-title')
                else:
                    # Clearbit placeholder for the rest just using the cleaned up name 
                    # If we don't have it, we leave it without tvg-logo, and let Android handle it with DiceBear
                    pass
        new_lines.append(line)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
if __name__ == "__main__":
    process_m3u("playlist_working.m3u8")
