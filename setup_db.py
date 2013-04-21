import sqlite3 as lite


def setup():

	appointment = """
	CREATE TABLE IF NOT EXISTS appointment (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
	    card_num    INTEGER,    -- 9 digit card number
	    apt_date    TEXT,       -- http://www.sqlite.org/lang_datefunc.html
	    hour		INTEGER,
	    minute		INTEGER		-- 0, 15, 30 or 45
	)"""


	db = lite.connect('data.db')
	c = db.cursor()

	c.execute(appointment)
	db.commit()

	c.close()
	db.close()

