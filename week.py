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

            if n != "h3" and not days and not self.getDaysOfWeek(unicode(tag)):
                self.headers.append(unicode(tag).strip())

            if n == "b":
                daysOfWeek = self.getDaysOfWeek(tag.get_text())
                if daysOfWeek:
                    days.extend(daysOfWeek)
                    currDay = daysOfWeek[-1]

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

    def getDaysOfWeek(self, text):
        return [Day(d) for d in dayNames if d in text]

class Day(object):
    def __init__(self, name):
        self.name = name
        self.num = dayNums[name]
        self.headers = []
        self.workouts = []

    def __str__(self):
        return "Day({name},{num})".format(name=self.name, num=self.num)

    def __repr__(self):
        return "Day({name},{num})".format(name=self.name, num=self.num)

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
