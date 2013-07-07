
import requests
import queries
import os
import psycopg2
from datetime import datetime as dt

""" Called by a cron job to trigger the appointments at the packaging center.
"""
now = dt.today()


def connect_db():
    pg_host    = os.getenv('PG_HOST')
    pg_db      = os.getenv('PG_DB')
    pg_user    = os.getenv('PG_USER')
    pg_pass    = os.getenv('PG_PASSWORD')
    db_connection_str = "host='{}' dbname='{}' user='{}' password='{}'".format(
        pg_host, pg_db, pg_user, pg_pass)
    return psycopg2.connect(db_connection_str)


def close_db(db):
    db.close()


def trigger_pickup(db, data):
    """ Uses a POST request to connect to the Ricoh server and trigger a single
        pickup.
    """
    uni, card_num = data[1:3]

    # interact with ricoh

    print "packages for {} triggered at {}".format(uni, now)
    queries.log_appointment(db, uni, card_num, dt.today())

def log(reservations):
    with open('log.txt', 'a+') as f:
        f.write(str(now)+'\n')
        for pickup in reservations:
            f.write('\t'+str(pickup[1])+'\n')


if __name__ == '__main__':
    db = connect_db()

    if now.minute >= 45:
        if now.hour == 23:
            slot = dt(now.year, now.month, now.day+1, 0, 0)
        else:
            slot = dt(now.year, now.month, now.day, now.hour+1, 0)
    else:
        slot = dt(now.year, now.month, now.day, now.hour, (now.minute/15+1)*15)
    print slot

    reservations = queries.get_time_slot(db, slot)
    for row in reservations:
        trigger_pickup(db, row)

    log(reservations)
    close_db(db)

