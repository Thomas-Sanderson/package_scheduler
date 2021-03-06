
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


def room_for_appointment(timeslot):
    # Makes a last chance check that there is still a slot available for the
    # chosen timeslot.
    # timeslot : datetime object
    return queries.check_time_slot(g.db, timeslot, g.week)


def check_other_appointments():
    # Check to see if the user has already made an appointment
    data = queries.check_for_uni(g.db, session['uni'])
    if len(data) == 0:
        return None
    else:
        date = data[0][2]
        time = data[0][3]
        message = ('Sorry, {}, you already have a reservation for {}/{} '
            +'at {}:{}')
        message = message.format(session['uni'],date.month, date.day, time.hour, time.minute)
        print message
        return message


@app.route('/reservation')
def success():
    return render_template('success.html')


@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if 'package' not in session or session['package'] == False:
        print 'oops'
        message = ("Sorry, you can't access the appointment page unless you have" 
            " a package waiting for you.")
        flash(unicode(message), 'error')
        return redirect(url_for('home'))

    other_appointment = check_other_appointments()
    if other_appointment != None:
        flash(unicode(other_appointment), 'error')
        return redirect(url_for('home'))

    # Loads the main screen that displays all of the timeslots. Their
    # availablilities will be represented in a heat map fashion.
    if request.method == 'GET':
        first = date.today()+timedelta(days=1)
        days = []
        for i in range(4):
            if g.week.empty(i) != True:
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
        print 'UNI:', session['uni']
        if room_for_appointment(slot) == False:
            flash(u'Sorry, that slot is no longer available', 'error')
            return redirect(url_for('appointment'))

        queries.make_appointment(g.db, session['uni'], slot)
        return redirect(url_for('success'))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uni = request.form['uni']
        session['uni'] = uni
        if has_package(request.form['uni']):
            return redirect(url_for('appointment'))
        else:
            flash("Sorry, "+uni+", you don't have a package right now", 'error')
            return redirect(url_for('home'))
    else:   # GET
        return render_template('home.html')


if __name__ == '__main__':
    app.run()

