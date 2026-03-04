import requests
from bs4 import BeautifulSoup

def scrape_football():
    url = "https://www.cardboardconnection.com/football-cards"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    releases = []
    for item in soup.select(".post"):
        title = item.select_one("h2").text.strip()
        link = item.select_one("a")["href"]
        desc_tag = item.select_one("p")
        desc = desc_tag.text.strip() if desc_tag else "Football card release"

        releases.append({
            "title": title,
            "url": link,
            "description": desc
        })

    return releases
