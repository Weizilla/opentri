""" Parses a week page into individual days"""

import argparse
from bs4 import BeautifulSoup
import mechanize
import os
import re
from local import LocalSource

dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dayNums = {day : num for num, day in enumerate(dayNames)}
removes = ["font", "hr", "div", "br", "center", "p", "h3"]
workoutPattern = "((?:SWIM|BIKE|RUN) \d+:\d+)"
replaces = [("\n", " ")]

def createTag(html, name, string):
    tag = html.new_tag(name)
    tag.string = string
    return tag

class Week(object):
    def __init__(self, source):
        self.num = source.num
        self.url = source.url
        html = self.read()
        self.clean(html)
        self.addTags(html)
        self.headers, self.headerLong = self.parseHeader(html)
        self.days = sorted(self.parseDays(html), key=lambda x: x.num)

    def read(self):
        if self.url.startswith("http"):
            html = mechanize.Browser().open(self.url).get_data()
        elif os.path.isfile(self.url):
            with open(self.url) as htmlFile:
                html = htmlFile.read()
        else:
            raise ValueError("Invalid source {}".format(self.url))

        html = html.decode("utf-8")
        for replace in replaces:
            html = html.replace(*replace) 
            html = html.replace(replace[0].upper(), replace[1]) 
        return BeautifulSoup(html)

    def clean(self, html):
        for remove in removes:
            [r.unwrap() for r in html(remove)]
        [a.decompose() for a in html("a", attrs={"name": True})]
        self.fixTwoDayTags(html)
        self.fixInvalidDayNames(html)
        return html

    def addTags(self, html):
        for tag in html("b"):
            text = tag.get_text()
            match = re.search(workoutPattern, text)
            if match:
                newTag = html.new_tag("span")
                newTag["class"] = match.group(1).split(" ")[0].lower()
                newTag.string = text
                tag.clear()
                tag.append(newTag)

    def parseHeader(self, html):
        text = unicode(html)

        regex = r"Swim (?P<s>\d+:\d+) - Bike (?P<b>\d+:\d+) - Run (?P<r>\d+:\d+) -- Total: (?P<t>\d+:\d+)"
        match = re.search(regex, text)
        headers = ["{s} {b} {r}".format(**(match.groupdict())), "Total {t}".format(**match.groupdict())] if match else []

        regex = r"Ultra Distance (?:Group|Training)(.*)<b>Monday</b>"
        match = re.search(regex, text)
        headerLong = match.group(1).strip() if match else None

        return headers, headerLong

    def parseDays(self, html):
        days = []

        text = unicode(html)

        regex = "(.*)".join("<b>" + d + "</b>" for d in dayNames) + "(.*)</body>"
        match = re.search(regex, text)
        if match:
            for i, workout in enumerate(match.groups()):
                day = Day(i)
                headers = re.findall(workoutPattern, workout)
                if headers:
                    day.headers.extend(headers)
                day.workouts.append(workout.strip())
                days.append(day)
        else:
            print text
            print regex

        return days

    def getAnchors(self, html):
        return (a for a in (Anchor(tag) for tag in html("b")) if a.days)

    def fixTwoDayTags(self, html):
        for anchor in self.getAnchors(html):
            numDays = len(anchor.days)
            if numDays == 2:
                self.fixTwoDayTag(anchor, html)
            elif numDays > 2:
                raise ValueError("More than two days in a single tag:" + unicode(anchor.tag))

    def fixTwoDayTag(self, anchor, html):
        tag = anchor.tag
        days = anchor.days
        text = tag.get_text()
        for day in days:
            text = text.replace(day, "")
        tag.clear()
        tag.append(createTag(html, "b", days[0]))
        tag.append(text.strip())
        tag.append(createTag(html, "b", days[1]))
        tag.unwrap()

    def fixInvalidDayNames(self, html):
        for anchor in self.getAnchors(html):
            if len(anchor.days) == 1:
                anchor.tag.string.replace_with(anchor.days[0])
            else:
                raise ValueError("More than one day in single tag:" + unicode(anchor.tag))

class Anchor(object):
    def __init__(self, tag):
        self.tag = tag
        self.days = [d for d in dayNames if d in tag.get_text()]

    def __repr__(self):
        return "Anchor({t},{d})".format(t=self.tag, d=self.days)

class Day(object):
    def __init__(self, num):
        self.name = dayNames[num]
        self.num = num
        self.headers = []
        self.workouts = []

    def __str__(self):
        return "Day({name},{num})".format(name=self.name, num=self.num)

    def __repr__(self):
        return "Day({name},{num})".format(name=self.name, num=self.num)

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="The source to parse")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    source = LocalSource(args.source).weeks[0]
    week = Week(source)
    print week.headers
    print "-----------------------"
    print week.headerLong
    print "============================="
    for day in week.days:
        print day.num, day.name
        print "--------------"
        print "\n".join(day.headers)
        print "--------------"
        print "\n".join(day.workouts)
        print "====================================="
