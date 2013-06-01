
import datetime as dt
from config import allotment


def next_week_appointments(db_conn):
    """ Returns all appointments from the next week.
    """
    now = dt.date.today()

    query_str = """
    SELECT  *
    FROM    appointments A
    WHERE   A.appointment_date >= '{}'
        AND A.appointment_date < '{}'
    ORDER   BY A.appointment_date;
    """.format(now.isoformat(), (now+dt.timedelta(days=7)).isoformat())
    print query_str


def check_time_slot(db, timeslot, week):
    """ checks if there are still spots open in the time slot
        return True if there's space
        return False if full
        timeslot is a datetime object
    """
    query_str = """
    SELECT  COUNT(*)
    FROM    appointments A
    WHERE   A.appointment_date = '{}'
        AND A.time = '{};'
    """.format(timeslot.strftime('%Y-%m-%d'),
               timeslot.strftime('%H:%M'))
    cursor = db.cursor()
    cursor.execute(query_str)
    num = cursor.fetchall()
    print num[0][0]

    days = (timeslot-dt.datetime.today()).days
    hours = timeslot.hour
    minutes = timeslot.minute/15
    slots = week.slots[days][hours][minutes]

    if num < slots:     # open spots
        return True
    else:               # filled up
        return False

