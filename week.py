""" Parses a week page into individual days"""

import argparse
import re
from bs4 import BeautifulSoup
from itertools import tee, izip

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", None]

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class Week(object):
    def __init__(self, htmlFile):
        with open(htmlFile) as file:
            self.soup = BeautifulSoup(file)
        self.parse()

    def parse(self):
        self.days = []
        text = self.soup.get_text()
        for startDay, endDay in pairwise(days):
            start = text.index(startDay)
            if endDay:
                end = text.index(endDay)
                workout = text[start:end]
            else:
                workout = text[start:]
            self.days.append(Day(startDay, workout.strip()))

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
    for day in week.days:
        print day.day
        print day.workout
        print "====================================="
