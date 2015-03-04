class WeekSource(object):
    def __init__(self, num, url):
        self.url = url
        self.num = int(num)

    def __str__(self):
        return "WeekSource({n},{u})".format(n=self.num,u=self.url)

    def __repr__(self):
        return "WeekSource({n},{u})".format(n=self.num,u=self.url)