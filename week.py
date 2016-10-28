""" Parses a week page into individual days"""

import argparse
from bs4 import BeautifulSoup
import mechanize
import os
import re
import json
from local import LocalSource
from day import DayParser, dayNames

removes = ["font", "hr", "div", "br", "center", "p", "h3"]
replaces = [("\n", " ")]
dayRegex = "(.*)".join("<b>" + d + "</b>" for d in dayNames) + "(.*)</body>"
workoutPattern = "((?:SWIM|BIKE|RUN) \d+:\d+)"

def createTag(html, name, string):
    tag = html.new_tag(name)
    tag.string = string
    return tag

class WeekParser(object):
    def parse(self, source):
        self.num = source.num
        self.url = source.url
        text = self.clean(source.text)
        html = BeautifulSoup(text, "html.parser")
        self.fixHtml(html)
        self.addTags(html)

        week = Week()
        week.weekNum = source.num
        week.id = "week-{n}".format(n=source.num)
        week.url = source.url
        week.weekTotals, week.weekHeader = self.parseHeader(html)
        week.days = sorted(self.parseDays(html), key=lambda x: x.id)
        return week

    def clean(self, text):
        for replace in replaces:
            text = text.replace(*replace) 
            text = text.replace(replace[0].upper(), replace[1]) 
        return text

    def fixHtml(self, html):
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
        regex = r"Swim (?P<swim>\d+:\d+) - Bike (?P<bike>\d+:\d+) - Run (?P<run>\d+:\d+) -- Total: (?P<total>\d+:\d+)"
        match = re.search(regex, text)
        totals = match.groupdict() if match else []
        regex = r"Ultra Distance (?:Group|Training)(.*)<b>Monday</b>"
        match = re.search(regex, text)
        header = match.group(1).strip() if match else None
        return totals, header

    def parseDays(self, html):
        dayParser = DayParser(self.num)
        days = []
        match = re.search(dayRegex, unicode(html))
        if match:
            for i, workout in enumerate(match.groups()):
                day = dayParser.parse(i, workout)
                days.append(day)
        else:
            print text, regex
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

class Week(object):
    pass

class Anchor(object):
    def __init__(self, tag):
        self.tag = tag
        self.days = [d for d in dayNames if d in tag.get_text()]

    def __repr__(self):
        return "Anchor({t},{d})".format(t=self.tag, d=self.days)

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="The source to parse")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    source = LocalSource(args.source).weeks[0]
    weekParser = WeekParser()
    week = weekParser.parse(source)
    print json.dumps(week.__dict__)
