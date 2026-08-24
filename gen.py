import os
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image


def sanitize(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).replace(' ', '_')


def get_app_id(url):
    res = re.search(r'/app/(\d+)', url)
    assert res
    return res.group(1)


def scrape_game_name(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    elem = soup.find('div', class_='apphub_AppName') or soup.find('title')
    assert elem
    return elem.text.strip().replace(' on Steam', '')


def download_capsule(app_id, path):
    soup = BeautifulSoup(requests.get(f"https://store.steampowered.com/app/{app_id}/").text, 'html.parser')
    img = soup.find('img', src=re.compile(rf'apps/{app_id}/.*header'))
    assert img, f"No capsule found for app {app_id}"
    r = requests.get(img['src'])
    assert r.status_code == 200
    with open(path, 'wb') as f:
        f.write(r.content)


def download_tall(app_id, path):
    """Portrait 600x900 library capsule. Not all apps have one."""
    r = requests.get(f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{app_id}/library_600x900.jpg")
    if r.status_code != 200:
        return
    with open(path, 'wb') as f:
        f.write(r.content)


def scale_and_crop(img, target_w, target_h, zoom=1.0, top=False):
    # top=True: fill + crop, anchored to top. top=False: fit whole image, black bars.
    fit = min if not top else max
    ratio = fit(target_h / img.height, target_w / img.width) * zoom
    img = img.resize((max(1, int(img.width * ratio)), max(1, int(img.height * ratio))), Image.LANCZOS)
    out = Image.new('RGB', (target_w, target_h))
    y = 0 if top else (target_h - img.height) // 2
    out.paste(img, ((target_w - img.width) // 2, y))
    return out


def pick(folder, n, tall):
    p = f"{folder}/game{n}_tall.png"
    return p if tall and os.path.exists(p) else f"{folder}/game{n}.png"


def create_bundle_image(folder, out_w, out_h, name, zoom_1=1.0, zoom_2=1.0, tall=False):
    game1 = Image.open(pick(folder, 1, tall))
    game2 = Image.open(pick(folder, 2, tall))

    game_w = out_w // 2
    g1 = scale_and_crop(game1, game_w, out_h, zoom_1, tall)
    g2 = scale_and_crop(game2, out_w - game_w, out_h, zoom_2, tall)

    result = Image.new('RGB', (out_w, out_h))
    result.paste(g1, (0, 0))
    result.paste(g2, (game_w, 0))
    result.save(f"{folder}/{name}.png")


def gen(url1, url2, zoom_1=1.0, zoom_2=1.0):
    game1, game2 = scrape_game_name(url1), scrape_game_name(url2)
    print(f"Game 1: {game1}\nGame 2: {game2}")

    folder = f"{sanitize(game1)}_x_{sanitize(game2)}"
    os.makedirs(folder, exist_ok=True)
    print(f"Created: {folder}")

    download_capsule(get_app_id(url1), f"{folder}/game1.png")
    download_capsule(get_app_id(url2), f"{folder}/game2.png")
    download_tall(get_app_id(url1), f"{folder}/game1_tall.png")
    download_tall(get_app_id(url2), f"{folder}/game2_tall.png")
    print("Downloaded capsules")

    create_bundle_image(folder, 1414, 464, "package_header", zoom_1, zoom_2)
    create_bundle_image(folder, 920, 430, "header_capsule", zoom_1, zoom_2, tall=True)
    create_bundle_image(folder, 462, 174, "small_capsule", zoom_1, zoom_2)
    create_bundle_image(folder, 1232, 706, "main_capsule", zoom_1, zoom_2, tall=True)
    print("Created bundle images")




LOOTPLOT = "https://store.steampowered.com/app/3057190/LOOTPLOT/"
CATX11 = "https://store.steampowered.com/app/4173020/CAT_CAT_CAT_CAT_CAT_CAT_CAT_CAT_CAT_CAT_CAT/",


# In future, other programs will call `generate`.
# So please leave this API as is; don't add `input()` or anything weird.
gen(
    LOOTPLOT,
    "https://store.steampowered.com/app/3282420/Zoominoes/",
)



