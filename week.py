""" Parses a week page into individual days"""

import argparse
from bs4 import BeautifulSoup
import mechanize
import os
import re
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
        self.headers = self.parseHeader(html)
        self.days = sorted(self.parseDays(html), key=lambda x: x.num)

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

    def parseHeader(self, html):
        headers = []

        return headers

    def parseDays(self, html):
        days = []

        tags = (day for tag in html("b") for day in self.getDaysOfWeek(tag))
        dayAnchors = {dayTag.name : dayTag for dayTag in tags}
        for day in dayAnchors.values():
            day.tag.string.replace_with(day.name)

        text = unicode(html)

        regex = "(.*)".join("<b>" + d + "</b>" for d in dayNames) + "(.*)</body>"
        match = re.search(regex, text)
        if match:
            print "\n".join(match.groups())

        return days

    def getDaysOfWeek(self, tag):
        text = tag.get_text()
        return [DayTag(d, tag) for d in dayNames if d in text]

class DayTag(object):
    def __init__(self, name, tag):
        self.name = name
        self.tag = tag

    def __repr__(self):
        return "DayTag({n},{t})".format(n=self.name, t=self.tag)

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
    # print week.headers
    # print "============================="
    # for day in week.days:
    #     print day.num, day.name
    #     print "--------------"
    #     print day.headers
    #     print "--------------"
    #     print day.workouts
    #     print "====================================="
