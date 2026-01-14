import os
import re
import requests
from bs4 import BeautifulSoup


def sanitize(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).replace(' ', '_')


def scrape_game_name(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    elem = soup.find('div', class_='apphub_AppName') or soup.find('title')
    assert elem
    return elem.text.strip().replace(' on Steam', '')


def gen(url1, url2):
    game1, game2 = scrape_game_name(url1), scrape_game_name(url2)
    print(f"Game 1: {game1}\nGame 2: {game2}")

    folder = f"{sanitize(game1)}_x_{sanitize(game2)}"
    os.makedirs(folder, exist_ok=True)
    print(f"Created: {folder}")



# In future, other programs will call `generate`.
# So please leave this API as is; don't add `input()` or anything weird.
gen(
    "https://store.steampowered.com/app/1404850/Luck_be_a_Landlord/",
    "https://store.steampowered.com/app/3385370/Maze_Mice/"
)


