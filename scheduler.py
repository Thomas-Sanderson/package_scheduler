
from flask import Flask, render_template, request, flash, \
    url_for, g, redirect, session
import queries
import week
import psycopg2
from datetime import date, datetime, timedelta
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
    # Connects to the DB and returns the db connection
    return psycopg2.connect(db_connection_str)


def close_db():
    # Closes DB connections and cursor
    g.db.close()


def has_package(uni):
    # Determines if a user has a package waiting for them.
    # Needs to implement a request to the Ricoh database.
    package = ricoh.package_info(uni)
    session["package"] = (True if package else False)
    return package

def room_for_appointment(week, timeslot):
    # Makes a last chance check that there is still a slot available for the
    # chosen timeslot.
    # timeslot : datetime object
    pass

@app.route('/reservation')
def success():
    return render_template('success.html')


@app.route('/appointment', methods=['GET', 'POST'])
def appointment():

    if 'package' not in session or session['package'] == False:
        print 'oops'
        flash("Sorry, you can't access the appointment page unless you have"+
            " a package waiting for you.")
        # TODO: figure out why message is flashed twice
        return redirect(url_for('home'))

    # Loads the main screen that displays all of the timeslots. Their
    # availablilities will be represented in a heat map fashion.
    if request.method == 'GET':
        first = date.today()+timedelta(days=1)
        days = []
        for i in range(4):
            days.append(first+timedelta(days=i))

        # PASSED IN VALUES: days = 4 relevant dates, week = week object
        return render_template('choose.html', days=days, week=g.week.slots)

    # Logs the appointment and inserts the new appointment to the database.
    # Before logging must call room_for_appointments() to avoid overbooking.
    else:
        # TODO: refactor
        choice = request.form["choice"].replace('[','').replace(']','')
        choice = choice.replace('(','').replace(')','').split(',')
        for i in range(len(choice)):
            choice[i] = int(choice[i].encode('ascii','ignore').strip())

        day = date.today() + timedelta(days=choice[0]+1)
        slot = datetime(day.year, day.month, day.day, choice[1], choice[2]*15)
        print slot
        print 'session', session['uni']
        # do last chance time slot check
        # TODO: fix card number shit
        queries.make_appointment(g.db, session['uni'], '2343', slot)
        return redirect(url_for('success'))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uni = request.form['uni']
        session['uni'] = uni
        if has_package(request.form['uni']):
            return redirect(url_for('appointment'))
        else:
            flash("Sorry, "+uni+", you don't have a package right now")
            return redirect(url_for('home'))
    else:   # GET
        return render_template('home.html')
    
if __name__ == '__main__':
    app.run()

