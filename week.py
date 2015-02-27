""" Parses a week page into individual days"""

import argparse
import re
from bs4 import BeautifulSoup
from itertools import tee, izip
from collections import OrderedDict
import mechanize
import os

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
removes = ["font", "hr", "div", "br"]
replaces = [("\n", " ")]

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class Week(object):
    def __init__(self, source, num=None):
        self.num = num
        self.read(source)
        self.clean()
        self.parse()

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
        self.days = OrderedDict()
        dayOfWeek = None
        for tag in self.html.html.body:
            n = tag.name
            if n == "b" and any(d in tag.string for d in days if tag.string):
                dayOfWeek = tag.string
                self.days[dayOfWeek] = Day(dayOfWeek)
            
            if dayOfWeek:
                self.days[dayOfWeek].workouts.append(tag)

                if n == "dl":
                    for t in tag.find_all("dt"):
                        self.days[dayOfWeek].headers.append(t.get_text().strip())

            if n == "b" and tag.string and "DAILY TOTAL" in tag.string:
                dayOfWeek = None

class Day(object):
    def __init__(self, day):
        self.day = day
        self.headers = []
        self.workouts = []

    def header(self):
        return "".join(unicode(s) for s in self.headers)

    def workout(self):
        return "".join(unicode(s) for s in self.workouts)

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="The source to parse")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    week = Week(args.source)
    for day in week.days.values():
        print day.day
        print "--------------"
        print day.header()
        print "--------------"
        print day.workout()
        print "====================================="
