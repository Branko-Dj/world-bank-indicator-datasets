from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os
import time

def removeQuestMarkAndAfter(link):
    link = re.sub('\?.+', '', link)
    return link

url = "https://data.worldbank.org/indicator?tab=featured"
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
sections = soup.find("div", {"class": "overviewArea body"}).findAll("section", {"class": "nav-item"})
ulList = list(map(lambda x: x.findAll("ul")[-1], sections))
liList = []
for ul in ulList:
    lis = ul.findAll("li")
    liList += lis

hrefList = list(map(lambda x: x.find("a").get("href"), liList))
links = list(map(lambda x: 'https://data.worldbank.org' + removeQuestMarkAndAfter(x), hrefList))
print(links[:10])

for link in links[:2]:
    os.system('python3 scripts/get.py ' + link)
    time.sleep(3)

indicatorList = os.listdir('indicators')
for indicator in indicatorList:
    os.system('data push ' + 'indicators/' + indicator)
    time.sleep(45)
