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
weekDelta = datetime.timedelta(weeks=1)
def weekStartGen():
    currWeek = startDate
    while True:
        yield currWeek
        currWeek += weekDelta

def createWeek(source):
    return Week(source)

class Generator(object):
    def __init__(self, source):
        self.source = source
        weeks = sorted(source.weeks, key=attrgetter("num"))
        pool = Pool(6)
        self.weeks = pool.map(createWeek, weeks)

    def generate(self, directory, filename):
        if not os.path.isdir(directory):
            os.makedirs(directory)
        path = os.path.join(directory, filename)

        startGen = weekStartGen()
        with open(path, "w") as output:
            weeks = "".join(self.genWeek(w, startGen.next()) for w in self.weeks)
            text = indexTemplate.substitute(weeks=weeks)
            output.write(text.encode('utf8'))
            print "Wrote {p}".format(p=path)

    def genWeek(self, week, start):
        header = self.genWeekHeader(week, start)
        days = "".join(self.genDay(d, week) for d in sorted(week.days, key=attrgetter("num")))
        subs = {"days": header + days,
                "weekId": "week-{w}".format(w=week.num),
                "weekName": "Week {w}".format(w=week.num),
                "weekStart": "{d.year}-{d.month}-{d.day}".format(d=start),
                "weekDate": "{d:%b} {d.day}".format(d=start),
                "weekUrl": week.url}
        return weekTemplate.substitute(subs)

    def genWeekHeader(self, week, start):
        subs = {"dayId": "week-{w}-h".format(w=week.num),
                "weekName": "Week {w} - {d:%b} {d.day}".format(w=week.num, d=start),
                "weekHeader": "<br/>".join(week.headers),
                "weekHeaderLong": week.headerLong}
        return weekHeaderTemplate.substitute(subs)

    def genDay(self, day, week):
        subs = {"dayId": "week-{w}-{d}".format(w=week.num, d=day.num),
                "dayName": day.name,
                "dayHeader": "<br/>".join(day.headers),
                "dayLong": "\n".join(day.workouts)}
        return dayTemplate.substitute(subs)

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
