from flask import Flask, render_template, request, flash, \
	url_for, g
import sqlite3 as lite
import requests
from allotment import allotment
import setup_db


app = Flask(__name__)
app.config.from_object('flask_settings')


"""
Connects to the DB and creates a cursor
"""
def connect_db():
   g.db = lite.connect('data.db')
   g.cursor = g.db.cursor()


"""
Closes DB connections and cursor
"""
def close_db():
    if hasattr(g, 'cursor'):
        g.c.close()
    if hasattr(g, 'db'):
        g.db.close()


"""
Uses a POST request to determine if the user has a package waiting for them
"""
def has_package():
    """
    TO BE IMPLEMENTED
    """
    return True


"""
Confirms that a user has a package
"""
def logged_in():
    if has_package():
        return redirect(url_for('appointment'))
    else:
        flash("Sorry, you don't have a pacakge waiting for you.")
        return redirect(url_for('home'))


"""
Logs the appointment into the database
"""
@app.route('/log_appointment', methods=['POST'])



@app.route('/schedule')
def appointment():


    return render_termplate('choose.html')
 

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    setup_db.setup()
    app.run()

