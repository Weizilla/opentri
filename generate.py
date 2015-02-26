"""Generates html pages for open tri workout"""
from string import Template
from opentri import OpenTri
import os
import datetime

def template(filename):
    with open(filename) as file:
        return Template(file.read())

dayTemplate = template("templates/day.html")
weekTemplate = template("templates/week.html")
indexTemplate = template("templates/index.html")

startDate = datetime.date(2015, 1, 5)

class Generator(object):
    def __init__(self, opentri):
        self.opentri = opentri

    def generate(self, directory, filename):
        if not os.path.isdir(directory):
            os.makedirs(directory)

        path = os.path.join(directory, filename)
        with open (path, "w") as output:
            weeks = ""
            weekGen = self.weekGen()
            for week in self.opentri.weeks:
                weekSubs = {}
                weekSubs["days"] = ""

                for day in week.days.values():
                    daySubs = {}
                    daySubs["dayName"] = "week{w}{d}".format(w=week.num, d=day.day)
                    daySubs["dayShort"] = day.day
                    daySubs["dayLong"] = day.workout.replace("\n", "<br>\n")
                    weekSubs["days"] += dayTemplate.substitute(daySubs)
                    print "Wrote week {w} day {d}".format(w=week.num, d=day.day) 

                weekSubs["weekId"] = "week{w}".format(w=week.num)
                weekSubs["weekName"] = "Week {w}".format(w=week.num)
                weekStart = weekGen.next()
                weekSubs["weekStart"] = "{d.year}-{d.month}-{d.day}".format(d=weekStart)
                weekSubs["weekDate"] = "{d:%b} {d.day}".format(d=weekStart)
                weeks += weekTemplate.substitute(weekSubs)
            
            text = indexTemplate.substitute(weeks=weeks)
            output.write(text)

    def weekGen(self):
        weekDelta = datetime.timedelta(weeks=1)
        def gen():
            currWeek = startDate
            while True:
                yield currWeek
                currWeek += weekDelta
        return gen()

if __name__ == "__main__":
    generator = Generator(OpenTri())
    generator.generate("html", "index.html")
