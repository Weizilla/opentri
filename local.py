"""Contains the source of links from a local directory"""
import os
from os.path import basename
import argparse
from weeksource import WeekSource

class LocalSource(object):
    def __init__(self, path):
        self.weeks = []
        if os.path.isdir(path):
            self.parseDir(path)
        elif os.path.isfile(path):
            self.parseFile(path)

    def parseDir(self, directory):
        for root, dirs, files in os.walk(directory):
            for filename in files:
                self.weeks.append(self.parseWeek(os.path.join(root, filename)))

    def parseFile(self, path):
        self.weeks = [self.parseWeek(path)]

    def parseWeek(self, path):
        filename = basename(path)
        weekNum = filename[filename.index("-") + 1:filename.index(".")]
        text = self.read(path)
        return WeekSource(weekNum, os.path.abspath(path), text)

    def read(self, path):
        with open(path) as htmlFile:
            return htmlFile.read().decode("utf-8")

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", "-p", default="target", help="The path to the file(s)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs();
    source = LocalSource(args.path)

    for week in source.weeks:
        print(week)
