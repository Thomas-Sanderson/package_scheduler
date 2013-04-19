
CREATE TABLE IF NOT EXISTS appointment (
    card_num    INTEGER,    -- 9 digit card number
    apt_date    TEXT,       -- http://www.sqlite.org/lang_datefunc.html
    apt_time    TEXT,
    PRIMARY KEY (card_num)
)

CREATE TABLE IF NOT EXISTS log (
    card_num    INTEGER,    -- 9 digit card number
    apt_date    TEXT,       -- http://www.sqlite.org/lang_datefunc.html
    apt_time    TEXT,
    PRIMARY KEY (card_num)
)
