import os
import glob
import json
import matplotlib.pyplot as plt
from datetime import datetime
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
        return f"{t.year}-{t.month:02d}-{t.day:02d}"

    def __str__(self):
        return f"{self.title()}"


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


def plot(by_date):
    dates = sorted(by_date.keys())
    plt.bar(dates, [len(by_date[d]) for d in dates])
    plt.title("Accepted submissions by date")
    plt.xlabel("Dates")
    plt.xlabel("Accepted submissions")
    plt.xticks(rotation=45)
    plt.show()


plot(load_submissions_by_date())
