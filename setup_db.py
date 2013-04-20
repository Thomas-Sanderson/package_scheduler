import sqlite3 as lite


def setup():

	appointment = """
	CREATE TABLE IF NOT EXISTS appointment (
	    card_num    INTEGER,    -- 9 digit card number
	    apt_date    TEXT,       -- http://www.sqlite.org/lang_datefunc.html
	    hour		INTEGER,
	    minute		INTEGER,		-- 0, 15, 30 or 45
	    PRIMARY KEY (card_num)
	)"""

	log = """
	CREATE TABLE IF NOT EXISTS log (
	    card_num    INTEGER,    -- 9 digit card number
	    apt_date    TEXT,       -- http://www.sqlite.org/lang_datefunc.html
	    hour		INTEGER,
	    minute		INTEGER,		-- 0, 15, 30 or 45
	    PRIMARY KEY (card_num)
	)"""

	db = lite.connect('data.db')
	c = db.cursor()

	c.execute(appointment)
	db.commit()

	c.execute(log)
	db.commit()

	c.close()
	db.close()

