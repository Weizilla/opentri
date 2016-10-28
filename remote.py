""" Downloads all of the pages into the target folder"""
import re
from operator import attrgetter
import os
import argparse
import mechanize
from bs4 import BeautifulSoup
from weeksource import WeekSource

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

class RemoteSource(object):
    def __init__(self):
        self.links = []
        self.br = mechanize.Browser()
        self.parseLinks()
        self.addNums()
        self.weeks = [WeekSource(l.num, l.url, self.open(l.url)) for l in self.links]

    def parseLinks(self):
        data = self.open(index)
        soup = BeautifulSoup(data)
        for a in soup.find_all("a"):
            link = self.parseLink(a)
            if link:
                self.links.append(link)

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

    def addNums(self):
        self.links = sorted(self.links, key=attrgetter("typeSort", "linkNum"))
        for i, l in enumerate(self.links):
            l.num = i + 1

    def save(self, directory):
        if not os.path.isdir(directory):
            os.makedirs(directory)

        for week in self.weeks:
            self.saveWeek(week, directory)

    def saveWeek(self, week, directory):
        data = self.open(week.url)
        filename = "Week-{n}.html".format(n=week.num)
        path = os.path.join(directory, filename)
        with open(path, "w") as output:
            output.write(data)
            print("Wrote {}".format(path))

class Link(object):
    def __init__(self, linkType, linkNum, url):
        self.linkType = linkType
        self.linkNum = linkNum
        self.url = url
        self.typeSort = typeSort[self.linkType]

    def __str__(self):
        return "Link({n},{t},{u})".format(t=self.linkType, n=self.linkNum, u=self.url)

    def __repr__(self):
        return "Link({n},{t},{u})".format(t=self.linkType, n=self.linkNum, u=self.url)

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--downloadDir", "-d", help="The directory to save the week pages to")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    source = RemoteSource()
    #for link in source.links:
    #    print link
    for week in source.weeks:
        print(week)

    if args.downloadDir:
        source.save(args.downloadDir)
