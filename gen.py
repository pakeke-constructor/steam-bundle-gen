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


def scale_and_crop(img, target_w, target_h):
    ratio = target_h / img.height
    new_w = int(img.width * ratio)
    img = img.resize((new_w, target_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    return img.crop((left, 0, left + target_w, target_h))


def make_outlined_cross(cross_img, size):
    OUTLINE_WIDTH = min(12, size//20)
    cross = cross_img.resize((size, size), Image.LANCZOS)

    # Make black version
    r, g, b, a = cross.split()
    black = Image.merge('RGBA', (a.point(lambda x: 0), a.point(lambda x: 0), a.point(lambda x: 0), a))

    # Canvas with padding for offsets
    result = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    # 8 directions for outline
    for dx, dy in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
        result.paste(black, (dx * OUTLINE_WIDTH, dy * OUTLINE_WIDTH), black)

    # White cross on top
    result.paste(cross, (0, 0), cross)
    return result


def create_bundle_image(folder, out_w, out_h, name):
    game1 = Image.open(f"{folder}/game1.png")
    game2 = Image.open(f"{folder}/game2.png")
    cross = Image.open("cross.png").convert("RGBA")

    game_w = out_w // 2
    cross = make_outlined_cross(cross, out_h // 2)
    g1 = scale_and_crop(game1, game_w, out_h)
    g2 = scale_and_crop(game2, game_w, out_h)

    result = Image.new('RGB', (out_w, out_h))
    result.paste(g1, (0, 0))
    result.paste(g2, (game_w, 0))
    cross_x = (out_w - cross.width) // 2
    cross_y = (out_h - cross.height) // 2
    result.paste(cross, (cross_x, cross_y), cross)
    result.save(f"{folder}/{name}.png")


def gen(url1, url2):
    game1, game2 = scrape_game_name(url1), scrape_game_name(url2)
    print(f"Game 1: {game1}\nGame 2: {game2}")

    folder = f"{sanitize(game1)}_x_{sanitize(game2)}"
    os.makedirs(folder, exist_ok=True)
    print(f"Created: {folder}")

    download_capsule(get_app_id(url1), f"{folder}/game1.png")
    download_capsule(get_app_id(url2), f"{folder}/game2.png")
    print("Downloaded capsules")

    create_bundle_image(folder, 1414, 464, "package_header")
    create_bundle_image(folder, 920, 430, "header_capsule")
    create_bundle_image(folder, 462, 174, "small_capsule")
    create_bundle_image(folder, 1232, 706, "main_capsule")
    print("Created bundle images")



# In future, other programs will call `generate`.
# So please leave this API as is; don't add `input()` or anything weird.
gen(
    "https://store.steampowered.com/app/1404850/Luck_be_a_Landlord/",
    "https://store.steampowered.com/app/3385370/Maze_Mice/"
)


