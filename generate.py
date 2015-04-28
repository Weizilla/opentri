"""Generates html pages for open tri workout"""
from string import Template
from local import LocalSource
from remote import RemoteSource
import os
import datetime
import argparse
from week import WeekParser
from operator import attrgetter
from multiprocessing import Pool
import json

startDate = datetime.date(2015, 1, 5)
weekDelta = datetime.timedelta(weeks=1)
def weekStartGen():
    currWeek = startDate
    while True:
        yield currWeek
        currWeek += weekDelta

def createWeek(source):
    parser = WeekParser()
    return parser.parse(source)

class Generator(object):
    def __init__(self, source):
        self.source = source

    def generate(self):
        pool = Pool(6)
        weeks = pool.map(createWeek, self.source.weeks)

        startGen = weekStartGen()
        self.weeks = sorted(weeks, key=lambda w: w.weekNum)
        for week in self.weeks:
            week.startDate = "{d.year}-{d.month}-{d.day}".format(d=startGen.next())
        return self.weeks

    def write(self, directory, filename):
        if not os.path.isdir(directory):
            os.makedirs(directory)

        path = os.path.join(directory, filename)
        with open(path, "w") as output:
            json.dump(self.weeks, output, 
                default=lambda o: o.__dict__, 
                indent=2, separators=(',', ': '))
            print "Wrote {p}".format(p=path)

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", "-l", help="Uses local directory for parsing")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    if args.local:
        source = LocalSource(args.local)
    else:
        source = RemoteSource()
    generator = Generator(source)
    generator.generate()
    generator.write("html", "workouts.json")
