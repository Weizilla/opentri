""" Parses a week page into individual days"""

import argparse
import re
from bs4 import BeautifulSoup
from itertools import tee, izip
from collections import OrderedDict
import mechanize
import os

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", None]

clean = ["<FONT FACE=\"Arial\">", "<FONT SIZE=-1>", "</FONT>", "<HR>", "</BODY>", "</HTML>"]

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class Week(object):
    def __init__(self, source, num=None, html=False):
        self.num = num
        self.read(source)
        self.clean(html)
        self.parse()

    def read(self, source):
        if source.startswith("http"):
            self.html = mechanize.Browser().open(source).get_data()
        elif os.path.isfile(source):
            with open(source) as htmlFile:
                self.html = htmlFile.read() 
        else:
            raise ValueError("Invalid source {}".format(source))

    def clean(self, html):
        if html:
            for cleanText in clean:
                self.text = self.html.replace(cleanText, "")
        else:
            self.text = BeautifulSoup(self.html).get_text().encode("utf-8")
        self.text = self.text.replace("\n\n", "\n")

    def parse(self):
        self.days = OrderedDict()
        for startDay, endDay in pairwise(days):
            start = self.text.index(startDay)
            if endDay:
                end = self.text.index(endDay)
                workout = self.text[start:end]
            else:
                workout = self.text[start:]
            self.days[startDay] = Day(startDay, workout.strip())

class Day(object):
    def __init__(self, day, workout):
        self.day = day
        self.workout = workout

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="The source to parse")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    week = Week(args.source)
    for day in week.days.values():
        print day.day
        print day.workout
        print "====================================="
