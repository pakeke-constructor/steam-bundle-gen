import requests
from bs4 import BeautifulSoup


def scrape_game_name(url: str) -> str:
    """Scrape the game name from a Steam store page URL."""
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Game name is in the apphub_AppName div
    name_elem = soup.find('div', class_='apphub_AppName')
    if name_elem:
        return name_elem.text.strip()

    # Fallback: try the page title
    title_elem = soup.find('title')
    if title_elem:
        # Steam titles are formatted as "Game Name on Steam"
        title = title_elem.text.strip()
        if ' on Steam' in title:
            return title.replace(' on Steam', '')
        return title

    raise ValueError(f"Could not find game name for URL: {url}")


def main(url1: str, url2: str):
    """Generate Steam bundle images from two game URLs."""
    game1_name = scrape_game_name(url1)
    game2_name = scrape_game_name(url2)

    print(f"Game 1: {game1_name}")
    print(f"Game 2: {game2_name}")


if __name__ == '__main__':
    url1 = input("Enter first Steam store URL: ")
    url2 = input("Enter second Steam store URL: ")
    main(url1, url2)
