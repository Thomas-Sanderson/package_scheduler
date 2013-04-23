from flask import Flask, render_template, request, flash, \
    url_for, g, redirect
from datetime import datetime, timedelta
import sqlite3 as lite
from allotment import allotment
import setup_db

num_days = 5


app = Flask(__name__)
app.config.from_object('package_app_settings')


def connect_db():
    """
    Connects to the DB and creates a cursor
    """
    g.db = lite.connect('data.db')
    g.cursor = g.db.cursor()


def close_db():
    """
    Closes DB connections and cursor
    """
    if hasattr(g, 'cursor'):
        g.cursor.close()
    if hasattr(g, 'db'):
        g.db.close()


def has_package():
    """
    Uses a POST request to determine if the user has a package waiting for them
    """
    """
    TO BE IMPLEMENTED
    """
    return True


def logged_in():
    """
    Confirms that a user has a package
    """
    if has_package():
        return redirect(url_for('appointment'))
    else:
        flash("Sorry, you don't have a pacakge waiting for you.")
        return redirect(url_for('home'))

# @app.route('/log_in', methods=['GET', 'POST'])
# def login():
#     if request.methods == 'POST'
#         session['card_num'] = request.form


@app.route('/schedule', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        """
        Logs the appointment into the database
        """
        sql_insert="INSERT INTO appointment VALUES ({},{},{},{})"
        #sql_insert.format(session['card_num'], )

        flash("Your appointment has been logged.")
        return redirect(url_for('home'))

    """
    Finds all appointments in the next 7 days by hour.
    """
    week = []
    now = datetime.today()
    for i in range(num_days):
        dt = now + timedelta(days=i)
        week.append("{}-{}-{}".format(dt.year, str(dt.month).zfill(2),
                    str(dt.day).zfill(2)))

    sql_query = """
    SELECT
        hour,
        minute,
        COUNT(*)
    FROM
        appointment
    WHERE
        apt_date == "{}"
    GROUP BY
        hour,
        minute
    ORDER BY
        hour,
        minute;
    """

    # [day][hour][minute][# appointments]
    appointments = [[[None for x in range(4)] for x in range(12)]
                    for x in range(num_days)]

    for i in range(num_days):
        for j in range(12):
            hour = str(j + 9)
            alloted = allotment[hour]
            for k in range(4):
                appointments[i][j][k] = alloted

    connect_db()
    for i in range(num_days):
        data = g.cursor.execute(sql_query.format(week[i])).fetchall()
        for segment in data:
            hour = segment[0]-9
            minute = segment[1]/15
            num_taken = segment[2]
            appointments[i][hour][minute] -= num_taken

    close_db()

    return render_template('choose.html', app=appointments, week=week)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    setup_db.setup()
    app.run()
