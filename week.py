""" Parses a week page into individual days"""

import argparse
import re
from bs4 import BeautifulSoup
from itertools import tee, izip
from collections import OrderedDict
import mechanize
import os

dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
daysOfWeek = {d : i for i, d in enumerate(dayNames)}
removes = ["font", "hr", "div", "br"]
replaces = [("\n", " ")]

class Week(object):
    def __init__(self, source, num=None):
        self.num = num
        self.source = source
        self.read(source)
        self.clean()
        self.parse()
        self.html = None
        del self.html

    def read(self, source):
        if source.startswith("http"):
            html = mechanize.Browser().open(source).get_data()
        elif os.path.isfile(source):
            with open(source) as htmlFile:
                html = htmlFile.read()
        else:
            raise ValueError("Invalid source {}".format(source))
        self.html = BeautifulSoup(html.decode("utf-8").replace("\n", " "))

    def clean(self):
        for remove in removes:
            [r.unwrap() for r in self.html(remove)]

    def parse(self):
        days = []
        currDay = None
        for tag in self.html.html.body:
            n = tag.name
            if n == "b":
                dayOfWeek = self.getDayOfWeek(tag) 
                if dayOfWeek: 
                    currDay = Day(dayOfWeek[0])
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
        self.days = sorted(days, key=lambda x: x.dayOfWeek)

    def getDayOfWeek(self, tag):
        if tag.string:
            return filter(lambda d: d in tag.string, dayNames)
        return None

class Day(object):
    def __init__(self, day):
        self.day = day
        self.dayOfWeek = daysOfWeek[day]
        self.headers = []
        self.workouts = []

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="The source to parse")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    week = Week(args.source)
    for day in week.days:
        print day.day
        print "--------------"
        print day.headers
        print "--------------"
        print day.workouts
        print "====================================="
