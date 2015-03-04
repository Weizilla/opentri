"""Generates html pages for open tri workout"""
from string import Template
from local import LocalSource
from remote import RemoteSource
import os
import datetime
import argparse
from week import Week
from operator import attrgetter
from multiprocessing import Pool

def template(filename):
    with open(filename) as file:
        return Template(file.read())

dayTemplate = template("templates/day.html")
weekTemplate = template("templates/week.html")
weekHeaderTemplate = template("templates/week-header.html")
indexTemplate = template("templates/index.html")

startDate = datetime.date(2015, 1, 5)

def createWeek(source):
    return Week(source)

class Generator(object):
    def __init__(self, source):
        self.source = source
        weeks = sorted(source.weeks, key=attrgetter("num"))
        pool = Pool(6)
        self.weeks = pool.map(createWeek, weeks)

    def generate(self, directory, filename):
        weekGen = self.weekGen()

        if not os.path.isdir(directory):
            os.makedirs(directory)

        path = os.path.join(directory, filename)
        with open(path, "w") as output:
            weeks = ""
            for week in self.weeks:
                weekStart = weekGen.next()
                weekSubs = {}

                weekHeaderSubs = {}
                weekHeaderSubs["dayId"] = "week-{w}-h".format(w=week.num)
                weekHeaderSubs["dayName"] = "Week {w}".format(w=week.num)
                weekHeaderSubs["dayHeader"] = "{d.year}-{d.month}-{d.day}".format(d=weekStart)
                weekHeaderSubs["dayLong"] = "<br/>".join(week.headers)

                weekSubs["days"] = weekHeaderTemplate.substitute(weekHeaderSubs)

                for day in sorted(week.days, key=lambda d: d.num):
                    daySubs = {}
                    daySubs["dayId"] = "week-{w}-{d}".format(w=week.num, d=day.num)
                    daySubs["dayName"] = day.name
                    daySubs["dayHeader"] = "<br/>".join(day.headers)
                    daySubs["dayLong"] = "\n".join(day.workouts)
                    weekSubs["days"] += dayTemplate.substitute(daySubs)

                weekSubs["weekId"] = "week-{w}".format(w=week.num)
                weekSubs["weekName"] = "Week {w}".format(w=week.num)
                weekSubs["weekStart"] = "{d.year}-{d.month}-{d.day}".format(d=weekStart)
                weekSubs["weekDate"] = "{d:%b} {d.day}".format(d=weekStart)
                weekSubs["weekUrl"] = week.url
                weeks += weekTemplate.substitute(weekSubs)

            text = indexTemplate.substitute(weeks=weeks)
            output.write(text.encode('utf8'))
            print "Wrote {p}".format(p=path)

    def weekGen(self):
        weekDelta = datetime.timedelta(weeks=1)
        def gen():
            currWeek = startDate
            while True:
                yield currWeek
                currWeek += weekDelta
        return gen()

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--localDirectory", "-l", help="Uses local directory for parsing")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    if args.localDirectory:
        source = LocalSource(args.localDirectory)
    else:
        source = RemoteSource()
    generator = Generator(source)
    generator.generate("html", "index.html")
