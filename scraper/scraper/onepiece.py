import requests
from bs4 import BeautifulSoup

def scrape_onepiece():
    url = "https://en.onepiece-cardgame.com/products/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    releases = []
    for item in soup.select(".productList li"):
        title = item.select_one(".title").text.strip()
        link = "https://en.onepiece-cardgame.com" + item.select_one("a")["href"]
        desc = item.select_one(".text").text.strip()

        releases.append({
            "title": title,
            "url": link,
            "description": desc
        })

    return releases
