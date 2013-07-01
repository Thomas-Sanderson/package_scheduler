
from flask import Flask, render_template, request, flash, \
    url_for, g, redirect
import queries
import week
import psycopg2
from datetime import date, timedelta
from os import getenv

import ricoh

app = Flask(__name__)
app.config.from_object('config.app_settings')

pg_host    = getenv('PG_HOST')
pg_db      = getenv('PG_DB')
pg_user    = getenv('PG_USER')
pg_pass    = getenv('PG_PASSWORD')
db_connection_str = "host='{}' dbname='{}' user='{}' password='{}'".format(
    pg_host, pg_db, pg_user, pg_pass)



@app.before_request
def before_request():
    g.db = connect_db()
    g.week = week.Week(queries.next_4day_appointments(connect_db()))


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        close_db()


def connect_db():
    """ Connects to the DB and returns the db connection
    """
    return psycopg2.connect(db_connection_str)


def close_db():
    """ Closes DB connections and cursor
    """
    g.db.close()



def has_package(uni):
    """ Determines if a user has a package waiting for them.
        Needs to implement a request to the Ricoh database.
    """
    return ricoh.package_info(uni)

def room_for_appointment(week, timeslot):
    """ Makes a last chance check that there is still a slot available for the
        chosen timeslot.
        timeslot : datetime object
    """
    pass


@app.route('/make_appointment', methods=['POST'])
def make_appointment():
    """ Logs the appointment and inserts the new appointment to the database.
        Before logging must call room_for_appointments() to avoid overbooking.
    """
    pass


@app.route('/appointment')
def appointment():
    """ Loads the main screen that displays all of the timeslots. Their
        availablilities will be represented in a heat map fashion.
    """

    first = date.today()+timedelta(days=1)
    days = []
    for i in range(4):
        days.append(first+timedelta(days=i))
    """ PASSED IN VALUES
        days = 4 relevant dates
        week = week object
    """
    return render_template('choose.html', days=days, week=g.week.slots)


@app.route('/')
def home():
    uni = request.args.get("uni")
    print uni
    if has_package(uni):
        return "T"
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
