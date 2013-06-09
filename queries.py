
import datetime as dt
from config import allotment


def next_week_appointments(db_conn):
    """ Returns all appointments from the next week.
        Starts with the appointments from tomorrow

        PARAMETERS:
        db_conn : postgres db connection
    """
    now = dt.date.today()

    query_str = """
    SELECT  A.appointment_date,
            A.time,
            COUNT(*) AS num
    FROM    appointments A
    WHERE   A.appointment_date > '{}'
        AND A.appointment_date <= '{}'
    GROUP   BY  A.appointment_date,
                A.time
    ORDER   BY  A.appointment_date asc,
                A.time asc;
    """.format(now.isoformat(), (now+dt.timedelta(days=7)).isoformat())
    cursor = db_conn.cursor()
    cursor.execute(query_str)
    db_conn.commit()
    data = cursor.fetchall()
    cursor.close()
    db_conn.close()
    for row in data:
        print row[0], row[1], int(row[2])
    return data


def check_time_slot(db_conn, timeslot, this_week):
    """ checks if there are still spots open in the time slot
        return True if there's space
        return False if full

        PARAMETERS:
        db_conn : postgres db connection
        timeslot : datetime
        this_week : Week object
    """
    query_str = """
    SELECT  COUNT(*)
    FROM    appointments A
    WHERE   A.appointment_date = '{}'
        AND A.time = '{};'
    """.format(timeslot.strftime('%Y-%m-%d'),
               timeslot.strftime('%H:%M'))
    cursor = db_conn.cursor()
    cursor.execute(query_str)
    num = cursor.fetchall()[0][0]
    cursor.close()

    days = (timeslot-dt.datetime.today()).days
    hours = timeslot.hour
    minutes = timeslot.minute/15
    slots = this_week.slots[days][hours][minutes]

    if num < slots:     # open spots
        return True
    else:               # filled up
        return False


def make_appointment(db_conn, uni, card_number, timeslot):
    """ Logs the new bookings into the appointments table in the db

        PARAMETERS:
        db_conn : postgres db connection
        uni : 6-7 character columbia identifier
        card_number : 9 character columbia id card number
        timeslot : datetime object representing the package appointment
    """

    insert_str = """
    INSERT INTO appointments
        (uni, card_number, appointment_date, time)
    VALUES
        ('{}',{},'{}','{}');
    """.format(uni, card_number, timeslot.strftime('%Y-%m-%d'),
               timeslot.strftime('%H:%M'))
    print insert_str
    cursor = db_conn.cursor()
    cursor.execute(insert_str)
    cursor.close()
    db_conn.commit()


def get_time_slot(db_conn, timeslot):
    """ Grabs all the appointments for the specified timeslot

        PARAMETERS:
        db_conn : postgres db connection
        timeslot : datetime
    """

    query_str = """
    SELECT  *
    FROM    appointments A
    WHERE   A.appointment_date = '{}'
        AND A.time = '{};'
    """.format(timeslot.strftime('%Y-%m-%d'),
               timeslot.strftime('%H:%M'))
    print query_str

    cursor = db_conn.cursor()
    cursor.execute(query_str)
    data = cursor.fetchall()
    cursor.close()

    return data

