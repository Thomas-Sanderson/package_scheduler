from flask import Flask, render_template, request, flash
import requests


app = Flask(__name__)
app.config.from_object('flask_settings')

def has_package():
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


@app.route('/schedule')
def appointment():
 
    return render_termplate('choose.html')
 



@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()



