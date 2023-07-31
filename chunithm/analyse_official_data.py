import os
import csv
import json
import xml.etree.ElementTree as ET
import requests
from tqdm import tqdm
import io

# setup proxy
PROXY = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}

# Your provided functions
def parse_music_data(xml_file, musicid):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    if root.find("./name/id").text != musicid:
        return None

    difficulties = {}

    for fumen in root.findall("./fumens/MusicFumenData"):
        if fumen.find("./enable").text.lower() == 'false':
            level = 0
        else:
            level = float(fumen.find("./level").text)
            level += float(fumen.find("./levelDecimal").text) / 100
        difficulty_type = fumen.find("./type/str").text.lower()
        if difficulty_type in ['expert', 'master', 'ultima']:
            difficulties[difficulty_type] = level

    return difficulties

def find_music_data(musicid, A000_dir, option_dir):
    # Search in A000 directory
    music_dir = os.path.join(A000_dir, 'music')
    music_id_dir = os.path.join(music_dir, f'music{musicid.zfill(4)}')
    if os.path.isdir(music_id_dir):
        xml_file = os.path.join(music_id_dir, 'Music.xml')
        if os.path.isfile(xml_file):
            return parse_music_data(xml_file, musicid)
    
    # Search in option directory
    for root, dirs, _ in os.walk(option_dir):
        for dir in dirs:
            music_dir = os.path.join(root, dir, 'music')
            if os.path.exists(music_dir):
                for item in os.listdir(music_dir):
                    item_path = os.path.join(music_dir, item)
                    if os.path.isdir(item_path):
                        xml_file = os.path.join(item_path, 'Music.xml')
                        if os.path.isfile(xml_file):
                            difficulties = parse_music_data(xml_file, musicid)
                            if difficulties is not None:
                                return difficulties

    return None

def download_image(image_id):
    url = f'https://new.chunithm-net.com/chuni-mobile/html/mobile/img/{image_id}'
    path = f'chunithm/jackets/{image_id}'

    if not os.path.exists(path):
        for i in range(3):  # try 3 times
            try:
                response = requests.get(url, proxies=PROXY)
                response.raise_for_status()  # if not 200, raise exception
                with open(path, 'wb') as file:
                    file.write(response.content)
                break
            except requests.RequestException:
                pass


def process_difficulty(value):
    if value == "":
        return 0.0
    else:
        return float(value[:-1]) + 0.5 if value.endswith("+") else float(value)


# Load json
with open("chunithm/music.json", 'r', encoding='utf-8') as f:
    musics = json.load(f)

# Load csv
csv_path = "chunithm/music_difficulties.csv"
if not os.path.exists(csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["musicid", "title", "expert", "master", "ultima"])

csv_data = {}

with open(csv_path, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        csv_data[row['musicid']] = {
            'expert': float(row['expert']) if row['expert'] else 0,
            'master': float(row['master']) if row['master'] else 0,
            'ultima': float(row['ultima']) if row['ultima'] else 0,
        }

A000_dir = 'D:/chunithm_sun_hdd/App/data/A000'
option_dir = 'D:/chunithm_sun_hdd/App/bin/option'
output_data = []

# Iterate musics
for music in tqdm(musics):
    musicid = music['id']
    difficulties = csv_data.get(musicid, None)

    if difficulties is None:
        difficulties = find_music_data(musicid, A000_dir, option_dir)

        if difficulties is None:
            csv_data[musicid] = {
                'expert': '',
                'master': '',
                'ultima': '',
            }
            with open(csv_path, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['musicid', 'title', 'expert', 'master', 'ultima'])
                writer.writerow({'musicid': musicid, 'title': music['title'], 'expert': '', 'master': '', 'ultima': ''})

    output_data.append({
        "name": music['title'],
        "id": musicid,
        "genreNames": [music['catname']],
        "jaketFile": music['image'],
        "difficulties": {
            "basic": process_difficulty(music['lev_bas']),
            "advanced": process_difficulty(music['lev_adv']),
            "expert": difficulties.get('expert', 0),
            "master": difficulties.get('master', 0),
            "ultima": difficulties.get('ultima', 0),
            "world's end": 0.0
        }
    })

    download_image(music['image'])

# Save output json
with io.open("chunithm/masterdata/musics.json", 'w', encoding='utf-8') as f:
    f.write(json.dumps(output_data, indent=4, ensure_ascii=False))