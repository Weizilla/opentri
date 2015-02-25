"""Generates html pages for open tri workout"""
from string import Template
from opentri import OpenTri
import os

def template(filename):
    with open(filename) as file:
        return Template(file.read())

dayTemplate = template("templates/day.html")
weekTemplate = template("templates/week.html")
indexTemplate = template("templates/index.html")

class Generator(object):
    def __init__(self, opentri):
        self.opentri = opentri

    def generate(self, directory, filename):
        if not os.path.isdir(directory):
            os.makedirs(directory)

        path = os.path.join(directory, filename)
        with open (path, "w") as output:
            weeks = ""
            for week in self.opentri.weeks:
                days = ""
                for day in week.days.values():
                    dayName = "week{w}{d}".format(w=week.num, d=day.day)
                    dayShort = day.day
                    dayLong = day.workout.replace("\n", "<br>\n")
                    days += dayTemplate.substitute(dayName=dayName, dayShort=dayShort, dayLong=dayLong)
                    print "Wrote week {w} day {d}".format(w=week.num, d=day.day) 
                weekName = "Week {w}".format(w=week.num)
                weeks += weekTemplate.substitute(weekName=weekName, days=days)
            
            text = indexTemplate.substitute(weeks=weeks)
            output.write(text)

if __name__ == "__main__":
    generator = Generator(OpenTri())
    generator.generate("html", "index.html")
