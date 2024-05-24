from argparse import ArgumentParser
import calendar
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


def last_day_of(year, month):
    return calendar.monthrange(year, month)[1]


def default_range():
    now = datetime.now()
    end_date = last_day_of(now.year, now.month)
    return [datetime(now.year, now.month, 1), datetime(now.year, now.month, end_date)]


def load_submissions_by_date(start, end):
    if not start or not end:
        start, end = default_range()
    result = defaultdict(set)
    for path in glob.glob(os.path.join("./local", "*.json")):
        with open(path) as f:
            dump = json.load(f)
            for data in dump["submissions_dump"]:
                sub = Submission(data)
                if not sub.is_accepted():
                    continue
                if not (start <= sub.submitted_date() <= end):
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


def main():
    def parse_date(s):
        return datetime.strptime(s, "%Y-%m-%d").date()

    parser = ArgumentParser(description="Leetcode Submissions")
    parser.add_argument(
        "-s", "--start", type=lambda s: parse_date(s), help="Start date"
    )
    parser.add_argument("-e", "--end", type=lambda s: parse_date(s), help="End date")

    args = parser.parse_args()
    plot(load_submissions_by_date(start=args.start, end=args.end))


if __name__ == "__main__":
    main()
