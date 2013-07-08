
import datetime as dt


def next_4day_appointments(db_conn):
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
    """.format(now.isoformat(), (now+dt.timedelta(days=4)).isoformat())
    cursor = db_conn.cursor()
    cursor.execute(query_str)
    db_conn.commit()
    data = cursor.fetchall()
    cursor.close()
    db_conn.close()
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

    if num <= slots:     # open spots
        return True
    else:               # filled up
        return False


def make_appointment(db_conn, uni, timeslot):
    """ Logs the new bookings into the appointments table in the db

        PARAMETERS:
        db_conn : postgres db connection
        uni : 6-7 character columbia identifier
        timeslot : datetime object representing the package appointment
    """
    cursor = db_conn.cursor()
    cursor.execute("""
    INSERT INTO appointments
        (uni, appointment_date, time)
    VALUES
        (%s,%s,%s);
    """,(uni, timeslot.strftime('%Y-%m-%d'),
               timeslot.strftime('%H:%M')))
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


def log_appointment(db_conn, uni, timeslot):
    """ Logs the triggered appointment into the 'triggered' table in the db

        PARAMETERS:
        db_conn : postgres db connection
        uni : 6-7 character columbia identifier
        timeslot : datetime object representing the time the appointment
                   was triggered
    """
    cursor = db_conn.cursor()
    cursor.execute("""
    INSERT INTO triggered
        (uni, appointment_date, time)
    VALUES
        (%s,%s,%s);
    """,(uni, timeslot.strftime('%Y-%m-%d'),
               timeslot.strftime('%H:%M')))
    cursor.close()
    db_conn.commit()


def check_for_uni(db_conn, uni):
    """ Checks to see if a certain uni has already made an appointment in the
        coming 4 days.
    """
    query_str = """
    SELECT *
    FROM appointments
    WHERE uni = '{}' AND
        appointment_date >= '{}' AND
        appointment_date < '{}';
    """.format(uni, dt.datetime.today().strftime('%Y-%m-%d'),
            (dt.datetime.today()+dt.timedelta(days=5)).strftime('%Y-%m-%d'))
    print query_str
    cursor = db_conn.cursor()
    cursor.execute(query_str)
    data = cursor.fetchall()
    cursor.close()
    print data
    return data

