import os
import glob
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict


class Submission:
    def __init__(self, data):
        self.data = data

    def title(self):
        return self.data["title"]

    def is_accepted(self):
        return self.data["status"] == 10

    def submitted_at(self):
        return datetime.fromtimestamp(self.data["timestamp"])

    def submitted_date(self):
        t = self.submitted_at()
        return datetime(t.year, t.month, t.day)

    def __str__(self):
        return f"{self.title()}"


def date_as_key(t):
    return f"{t.year}-{t.month:02d}-{t.day:02d}"


def load_submissions_by_date():
    result = defaultdict(set)
    for path in glob.glob(os.path.join("./local", "*.json")):
        with open(path) as f:
            dump = json.load(f)
            for data in dump["submissions_dump"]:
                sub = Submission(data)
                if not sub.is_accepted():
                    continue
                result[sub.submitted_date()].add(sub)
    return result


def days_between(start, end):
    cur = start
    result = []
    while cur <= end:
        result.append(cur)
        cur = cur + timedelta(days=1)
    return result


def plot(by_date):
    days = sorted(by_date.keys())
    days = days_between(days[0], days[-1])
    x = [date_as_key(day) for day in days]
    y = [len(by_date[day]) for day in days]

    plt.bar(x, y)
    plt.title("Accepted submissions by date")
    plt.xlabel("Dates")
    plt.xlabel("Accepted submissions")
    plt.xticks(rotation=45)
    plt.tight_layout(pad=2.0)
    plt.show()


plot(load_submissions_by_date())
