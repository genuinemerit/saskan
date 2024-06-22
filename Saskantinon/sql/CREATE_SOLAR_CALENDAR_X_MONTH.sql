CREATE TABLE IF NOT EXISTS SOLAR_CALENDAR_X_MONTH (
solar_calendar_x_moon_uid_pk TEXT DEFAULT '',
solar_calendar_uid_fk TEXT DEFAULT '',
month_uid_fk TEXT DEFAULT '',
FOREIGN KEY (solar_calendar_uid_fk) REFERENCES SOLAR_CALENDAR(solar_calendar_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (month_uid_fk) REFERENCES MONTH(month_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (solar_calendar_x_moon_uid_pk));
