
CREATE TABLE appointments (
    id                  SERIAL PRIMARY KEY,
    uni                 VARCHAR(7),
    card_number         INTEGER,
    appointment_date    DATE,
    hour                TIME
);

CREATE INDEX time_slot ON appointments(appointment_date,hour);


