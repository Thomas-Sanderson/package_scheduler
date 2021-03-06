
CREATE TABLE IF NOT EXISTS appointments (
    id                  SERIAL PRIMARY KEY,
    uni                 VARCHAR(7),
    appointment_date    DATE,
    time                TIME
);

CREATE INDEX time_slot ON appointments(appointment_date, time);

CREATE TABLE IF NOT EXISTS triggered (
    id                  SERIAL PRIMARY KEY,
    uni                 VARCHAR(7),
    appointment_date    DATE,
    time                TIME
);


