from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta

date = date.today() - timedelta(days = 1)

#p/1/
url = "https://www.oricon.co.jp/rank/js/d/" + date.strftime("%Y-%m-%d") + "/"

session = requests.Session()

def parsePage(url):
    result = []

    response = session.get(url)
    if response.status_code != 200:
        return result
    
    soup = BeautifulSoup(response.content, "html.parser")

    for section in soup.select("section"):
        data = section.select_one(".inner")
        if not data:
            continue

        title = data.select_one("h2").get_text(strip=True)
        artist = data.select_one("p.name").get_text(strip=True)
        result.append(f"{artist} - {title}")
    return result

def parseDay():
    tracks = []
    for i in range(1, 4):
        tracks.extend(parsePage(url + "p/" + str(i) + "/"))
    
    return tracks

test = parseDay()
print("\n".join(test))
