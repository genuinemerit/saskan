CREATE TABLE IF NOT EXISTS LUNAR_CALENDAR_X_MONTH (
lunar_calendar_x_moon_uid_pk TEXT DEFAULT '',
lunar_calendar_uid_fk TEXT DEFAULT '',
month_uid_fk TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
FOREIGN KEY (lunar_calendar_uid_fk) REFERENCES LUNAR_CALENDAR(lunar_calendar_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (month_uid_fk) REFERENCES MONTH(month_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (lunar_calendar_x_moon_uid_pk));
