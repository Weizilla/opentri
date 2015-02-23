""" Downloads all of the pages into the target folder"""
import mechanize
import re
from bs4 import BeautifulSoup
from operator import attrgetter, methodcaller

index = "http://opentri-training.com/free/ultra/"

typeRegex = {
    r"week([\d]+).htm" : "orientation",
    r"weekp([\d]+).htm" : "preseason",
    r"weekc([\d]+).htm" : "competitive",
    r"taper([\d]+).htm" : "taper"
}

typeSort = {
    "orientation" : 0,
    "preseason" : 1,
    "competitive" : 2,
    "taper" : 3
}

class OpenTri(object):
    def __init__(self):
        self.br = mechanize.Browser()
        self.getLinks()

    def getLinks(self):
        self.links = []
        data = self.open(index)
        soup = BeautifulSoup(data)
        for a in soup.find_all("a"):
            link = self.parseLink(a)
            if link:
                self.links.append(link)
        self.sort()

    def open(self, url):
        return self.br.open(url).get_data()

    def parseLink(self, a):
        text = a.get_text().replace("\n", "").replace("  ", " ")
        if text:
            url = a.get("href")
            linkType, num = self.getType(url)            
            if linkType:
                return Link(linkType, num, index + url)

    def getType(self, url):
        for (regex, linkType) in typeRegex.items():
            match = re.search(regex, url)
            if match:
                return linkType, int(match.group(1))
        return None, None

    def sort(self):
        self.links = sorted(self.links, key=attrgetter("typeSort", "linkNum"))
        for i, l in enumerate(self.links):
            l.num = i + 1

class Link(object):
    def __init__(self, linkType, linkNum, url):
        self.linkType = linkType
        self.linkNum = linkNum
        self.url = url
        self.typeSort = typeSort[self.linkType]

    def __str__(self):
        return "Link({n},{t},{u})".format(t=self.linkType,n=self.num, u=self.url)

    def __repr__(self):
        return "Link({n},{t},{u})".format(t=self.linkType,n=self.num, u=self.url)

if __name__ == "__main__":
    openTri = OpenTri()
    print "\n".join(str(s) for s in openTri.links)
