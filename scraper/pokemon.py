import requests
from bs4 import BeautifulSoup

def scrape_pokemon():
    url = "https://www.pokemon.com/us/pokemon-tcg/product-gallery"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    releases = []
    for card in soup.select(".product-item"):
        title = card.select_one(".product-title").text.strip()
        link = "https://www.pokemon.com" + card.select_one("a")["href"]
        desc = card.select_one(".product-description").text.strip()

        releases.append({
            "title": title,
            "url": link,
            "description": desc
        })

    return releases
