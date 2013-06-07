from flask import Flask, render_template, request, flash, \
    url_for, g, redirect

from config.allotment import current_week, next_week
import queries

from os import getenv
import psycopg2

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




def logged_in():
    """ Confirms that a user has a package
    """
    if has_package():
        return redirect(url_for('appointment'))
    else:
        flash("Sorry, you don't have a pacakge waiting for you.")
        return redirect(url_for('home'))


def has_package(uni):
    """ Determines if a user has a package waiting for them.
        Needs to implement a request to the Ricoh database.
    """
    pass


@app.route('/appointment')
def appointment():
    appointments = queries.next_week_appointments(g.db)

    return redirect(url_for('home'))
    #return render_template('choose.html')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()

