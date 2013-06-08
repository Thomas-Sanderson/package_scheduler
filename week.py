
from config import allotment
from datetime import date as dt_date
import queries


class Week:

    def __init__(self, appointments):
        """ Appointments is an array of the # of appointments for each
            available time slot.
            Starts with tomorrow.
        """
        week_array = []

        # creating array of appointments
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

        # limiting array to only the next 7 days
        self.now = dt_date.today().weekday()+1
        self.slots = week_array[self.now:self.now+7]

        # inserting appointments into the array for the week
        for date, time, num in appointments:
            day = (date-dt_date.today()).days-1
            hour = time.hour
            minute = time.minute/15
            if self.slots[day][hour][minute] != None:
                self.slots[day][hour][minute] -= int(num)


    def __str__(self):
        week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
                "sunday"]
        string = ""
        for a in range(7):
            hour = 0
            string += "{}\n".format(week[(a+self.now) % 7])
            string += "\t00\t15\t30\t45\n"
            for b in self.slots[a]:
                string += '{}\t'.format(hour)
                hour += 1
                for c in b:
                    string += "{}\t".format(c)
                string += '\n'
        return string

