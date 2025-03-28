from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta

date = date.today() - timedelta(days = 1)

#p/1/
url = "https://www.oricon.co.jp/rank/js/d/" + date.strftime("%Y-%m-%d") + "/"

def parsePage(url):
    result = []
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find_all("section")
    for section in sections:
        data = section.find("div", class_="inner")
        title = data.find("div").find("h2").text.strip()
        artist = data.find("div").find("p").text.strip()
        result.append(title + " - " + artist)
    return result

def parseDay():
    tracks = []
    for i in range(1, 4):
        tracks.extend(parsePage(url + "p/" + str(i) + "/"))
    
    return tracks

