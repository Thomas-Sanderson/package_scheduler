from flask import Flask, render_template, request, flash, \
    url_for, g, redirect
from allotment import allotment
import db_config

num_days = 5


app = Flask(__name__)
db_conn = 'postgresssql+psycopg2://{}:{}@{}/{}'.format(
            db_config.username, db_config.password, db_config.host, db_config.db);

app.config.from_object('package_app_settings')


def connect_db():
    """
    Connects to the DB and creates a cursor
    """
    pass


def close_db():
    """
    Closes DB connections and cursor
    """
    pass


def logged_in():
    """
    Confirms that a user has a package
    """
    if has_package():
        return redirect(url_for('appointment'))
    else:
        flash("Sorry, you don't have a pacakge waiting for you.")
        return redirect(url_for('home'))


def has_package():
    """
    Determines if a user has a package waiting for them.
    """
    pass


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    setup_db.setup()
    app.run()
