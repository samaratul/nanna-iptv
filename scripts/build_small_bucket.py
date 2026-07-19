import csv
import io
import re

user_data = """Main Category,Sub-Category,Representative Channels
Nepali,Entertainment,"Kantipur Max HD, Nari HD, Indreni TV, GNN, Prime TV"
Nepali,Movies,"A1 TV, Mega Gold, Kasthamandap Gold"
Nepali,Sports,"Himalaya Sports HD, Action Sports HD"
Nepali,News,"Nepal TV HD, NTV News/Plus HD, Kantipur HD, AP1 HD, Himalaya TV HD, News 24, Image HD, Sagarmatha TV, Avenues TV, ABC News, Mountain TV, Janata TV, Channel 4 Nepal"
Nepali,Infotainment/Other,"Indigenous Television, Nepal Mandal, Bodhi TV, Krishi TV, Business Plus, Dharma TV, Deep Television"
Hindi,Entertainment,"Star Plus HD, Star Bharat HD, Sony Entertainment (SET) HD, Sony SAB HD, Zee TV HD, Colors HD, &TV HD, Colors Rishtey, Zee Cafe"
Hindi,Movies,"Star Gold HD, Zee Cinema HD, Sony Max HD, &Pictures HD, Colors Cineplex HD, B4U Movies, Zee Anmol, Star Utsav, Sony PAL"
Hindi,Sports,"Star Sports 1/2/3/Select HD, Sony Ten 1/2/3/5 HD"
Hindi,News,"Aaj Tak, News 18, ABP News, NDTV 24x7, Zee News, India Today, WION"
English,Entertainment,"Comedy Central, AXN, Romedy Now"
English,Movies,"Star Movies HD, Star Movies Select HD, Sony Pix"
English,News,"BBC News, CNN, Al Jazeera HD, TRT World HD, France 24, CGTN News HD, RT English, ABC Australia"
English,Infotainment,"National Geographic HD, Nat Geo Wild HD, Discovery HD, Animal Planet HD, TLC, Sony BBC Earth HD, History TV18"
English,Kids,"Nickelodeon (Nick) HD, Nick Jr, Pogo, Cartoon Network HD+, Disney International HD, Sony YAY!, Hungama"
Bhojpuri,General/Entertainment,"TV Birgunj (Bilingual/Regional focus) [1.3.1, 1.3.3], Anjan TV, Manoranjan Prime, Manoranjan Grand"
Bhojpuri,Movies/Music,"B4U Bhojpuri [1.2.3, 1.2.4], Goldmines Bhojpuri [1.2.3, 1.2.4], Sangeet Bhojpuri [1.2.3, 1.2.4], Oscar Movies Bhojpuri"
"""

# Read existing streams to find URLs
public_streams = {} # lowercase channel name -> url
try:
    with open('bucket_public_working.m3u8', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        current_name = ""
        for line in lines:
            if line.startswith('#EXTINF'):
                current_name = line.split(',')[-1].strip()
            elif line.startswith('http') and current_name:
                public_streams[current_name.lower()] = line.strip()
                current_name = ""
except:
    pass

# Helper to find a stream url
def find_stream(target):
    # strip HD and bracketed/parenthesized metadata for looser matching
    clean_target = re.sub(r'\[.*?\]|\(.*?\)', '', target)
    clean_target = clean_target.replace('HD+', '').replace('HD', '').strip().lower()
    
    # if it's a bundled string like "Star Sports 1/2/3/Select HD", just try to find the first one
    if '/' in clean_target:
        clean_target = clean_target.split('/')[0].strip()
        
    for pub_name, url in public_streams.items():
        if clean_target in pub_name:
            return url
    return "http://offline.stream/playlist.m3u8"


reader = csv.reader(io.StringIO(user_data))
header = next(reader)

with open('playlist_working.m3u8', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    
    for row in reader:
        lang = row[0].strip()
        genre = row[1].strip()
        channels = [c.strip() for c in row[2].split(',')]
        
        f.write('\n# ======================\n')
        f.write(f'# {lang} - {genre}\n')
        f.write('# ======================\n')
        
        for ch in channels:
            url = find_stream(ch)
            f.write(f'#EXTINF:-1 group-title="{lang} - {genre}",{ch}\n')
            f.write(f'{url}\n')

print("Successfully generated exact mapping playlist_working.m3u8")
