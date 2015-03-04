""" Parses a week page into individual days"""

import argparse
from bs4 import BeautifulSoup
import mechanize
import os
from local import LocalSource

dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dayNums = {day : num for num, day in enumerate(dayNames)}
removes = ["font", "hr", "div", "br", "center"]
replaces = [("\n", " ")]

class Week(object):
    def __init__(self, source):
        self.num = source.num
        self.url = source.url
        html = self.read()
        self.clean(html)
        self.parse(html)

    def read(self):
        if self.url.startswith("http"):
            html = mechanize.Browser().open(self.url).get_data()
        elif os.path.isfile(self.url):
            with open(self.url) as htmlFile:
                html = htmlFile.read()
        else:
            raise ValueError("Invalid source {}".format(self.url))
        return BeautifulSoup(html.decode("utf-8").replace("\n", " "))

    def clean(self, html):
        for remove in removes:
            [r.unwrap() for r in html(remove)]
        return html

    def parse(self, html):
        days = []
        self.headers = []
        currDay = None
        for tag in html.html.body:
            n = tag.name

            if n != "h3" and not days and not self.getDayOfWeek(tag):
                self.headers.append(unicode(tag).strip())

            if n == "b":
                dayOfWeek = self.getDayOfWeek(tag)
                if dayOfWeek:
                    currDay = Day(dayOfWeek[0]) # handle multiple days in single tag
                    days.append(currDay)

            if currDay:
                text = unicode(tag).strip()
                if text:
                    currDay.workouts.append(text)

                if n == "dl":
                    for t in tag.find_all("dt"):
                        currDay.headers.append(t.get_text().strip())

            if n == "b" and tag.string and "DAILY TOTAL" in tag.string:
                currDay = None

        self.days = sorted(days, key=lambda x: x.num)

    def getDayOfWeek(self, tag):
        if tag.string:
            return filter(lambda d: d in tag.string, dayNames)
        return None

class Day(object):
    def __init__(self, name):
        self.name = name
        self.num = dayNums[name]
        self.headers = []
        self.workouts = []

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="The source to parse")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    source = LocalSource(args.source).weeks[0]
    week = Week(source)
    print week.headers
    print "============================="
    for day in week.days:
        print day.num, day.name
        print "--------------"
        print day.headers
        print "--------------"
        print day.workouts
        print "====================================="
