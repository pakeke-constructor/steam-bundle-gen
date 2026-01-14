import os
import re
import requests
from bs4 import BeautifulSoup


def sanitize(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).replace(' ', '_')


def get_app_id(url):
    return re.search(r'/app/(\d+)', url).group(1)


def scrape_game_name(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    elem = soup.find('div', class_='apphub_AppName') or soup.find('title')
    assert elem
    return elem.text.strip().replace(' on Steam', '')


def download_capsule(app_id, path):
    urls = [
        f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/capsule_616x353.jpg",
        f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{app_id}/header_2x.jpg",
        f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{app_id}/header.jpg",
    ]
    for url in urls:
        r = requests.get(url)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
            return


def gen(url1, url2):
    game1, game2 = scrape_game_name(url1), scrape_game_name(url2)
    print(f"Game 1: {game1}\nGame 2: {game2}")

    folder = f"{sanitize(game1)}_x_{sanitize(game2)}"
    os.makedirs(folder, exist_ok=True)
    print(f"Created: {folder}")

    download_capsule(get_app_id(url1), f"{folder}/game1.png")
    download_capsule(get_app_id(url2), f"{folder}/game2.png")
    print("Downloaded capsules")



# In future, other programs will call `generate`.
# So please leave this API as is; don't add `input()` or anything weird.
gen(
    "https://store.steampowered.com/app/1404850/Luck_be_a_Landlord/",
    "https://store.steampowered.com/app/3385370/Maze_Mice/"
)


