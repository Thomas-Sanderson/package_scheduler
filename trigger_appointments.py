
import requests
import queries
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

    with open('triggered.txt', 'w') as f:
        f.write("{}\n".format(dt.today().isoformat())

    queries.log_appointmen(db, uni, card_num, dt.today())


if __name__ == '__main__':
    db = connect_db()

    for row in data:
        trigger_pickup(db, row)

    close_db(db)

