
from random import randint
from sys import argv
import os
import psycopg2

def connect_db():
    pg_host    = os.getenv('PG_HOST')
    pg_db      = os.getenv('PG_DB')
    pg_user    = os.getenv('PG_USER')
    pg_pass    = os.getenv('PG_PASSWORD')
    db_connection_str = "host='{}' dbname='{}' user='{}' password='{}'".format(
        pg_host, pg_db, pg_user, pg_pass)
    print db_connection_str
    db = psycopg2.connect(db_connection_str)
    return db

if len(argv) != 2:
    print 'please pass in the number of rows you would like to produce!'
    print 'usuage:\tpython fake_data_maker.py <num rows>'
    exit(1)

if argv[1] == 'clear':
    db = connect_db()
    cursor = db.cursor()
    clear_str = "DELETE FROM appointments WHERE 0=0;"
    cursor.execute(clear_str)
    db.commit()
    cursor.close()
    db.close()
    print 'rows deleted from appointments'
    exit(0)


with open('fake_data.txt', 'w+') as f:
	for x in range(int(argv[1])):
	    uni = ''
	    for i in range(3):
	        uni += str(unichr(randint(ord('a'), ord('z'))))
	    uni += str(randint(1000, 9999))

	    appointment_date = "2013-07-{}".format(str(randint(1, 30)).zfill(2))
	    time = "{}:{}".format(str(randint(0, 23)).zfill(2), str(randint(0, 3)*15).zfill(2))

	    f.write("('{}', '{}', '{}')\n".format(uni, appointment_date, time))

db = connect_db()
cursor = db.cursor()

with open('fake_data.txt', 'r') as f:
    data = f.read().strip().split('\n')

insert_str = """
    INSERT INTO appointments (uni, appointment_date, time)
    VALUES """

group = 20

for index in range(len(data)/group+1):
    rows = data[index*group : (index+1)*group - 1]
    if len(rows) == 0:
        break
    temp = str(insert_str)
    temp += ', '.join(rows)
    temp += ';'
    print temp
    cursor.execute(temp)
    db.commit()

cursor.close()
db.close()

