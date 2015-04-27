""" Parses a block of html into a single day"""

import argparse
from bs4 import BeautifulSoup
import mechanize
import os
import re
from local import LocalSource
from collections import OrderedDict 

dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
totalsPattern = "((?:SWIM|BIKE|RUN) \d+:\d+)"

class DayParser(object):
    def __init__(self, weekNum):
        self.weekNum = weekNum

    def parse(self, dayNum, html):
        day = Day()
        day.id = "day-{w}-{d}".format(w=self.weekNum, d=(dayNum + 1))
        day.weekIndex = self.weekNum - 1
        day.weekNum = self.weekNum
        day.dayIndex = dayNum
        day.dayOfWeek = dayNames[dayNum]
        day.dayTotals = [d.split(" ") for d in re.findall(totalsPattern, html)] or []
        day.dayWorkout = html.strip()
        return day

class Day(object):
    pass
