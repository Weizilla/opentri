""" Parses a week page into individual days"""

import argparse
import re
from bs4 import BeautifulSoup
from itertools import tee, izip
from collections import OrderedDict

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", None]

clean = ["<FONT FACE=\"Arial\">", "<FONT SIZE=-1>", "</FONT>", "<HR>", "</BODY>", "</HTML>" ]

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class Week(object):
    def __init__(self, filename):
        with open(filename) as htmlFile:
            self.html = htmlFile.read() 
        self.clean()
        self.parse()

    def clean(self):
        for cleanText in clean:
            self.html = self.html.replace(cleanText, "")

    def parse(self):
        self.days = OrderedDict()
        for startDay, endDay in pairwise(days):
            startDayIndex = self.html.index(startDay)
            start = self.html.index("<BR>", startDayIndex)
            if endDay:
                endDayIndex = self.html.index(endDay)
                end = self.html.rindex("<DIV ALIGN=right>", startDayIndex, endDayIndex)
                workout = self.html[start:end]
            else:
                workout = self.html[start:]
            self.days[startDay] = Day(startDay, workout.strip())

class Day(object):
    def __init__(self, day, workout):
        self.day = day
        self.workout = workout

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename", help="The file to parse")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    week = Week(args.filename)
    for day in week.days.values():
        print day.day
        print day.workout
        print "====================================="
