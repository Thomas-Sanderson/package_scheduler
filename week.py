
from config import allotment
from datetime import date


class Week:

    def __init__(self, appointments=None):
        week_array = []
        self.now = date.today().weekday()

        for i in range(7):      # first week
            week_array.append([])
            for j in range(24):
                week_array[i].append([])
                for k in range(4):
                    week_array[i][j].append(allotment.current_week[i][j])
        for i in range(7, 14):   # second week
            week_array.append([])
            for j in range(24):
                week_array[i].append([])
                for k in range(4):
                    week_array[i][j].append(allotment.next_week[i % 7][j])

        self.slots = week_array[self.now:self.now+7]

    def __str__(self):
        week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
                "sunday"]
        string = ""
        for a in range(7):
            string += "{}\n".format(week[(a+self.now) % 7])
            for b in self.slots[a]:
                for c in b:
                    string += "{}\t".format(c)
                string += '\n'
        return string

