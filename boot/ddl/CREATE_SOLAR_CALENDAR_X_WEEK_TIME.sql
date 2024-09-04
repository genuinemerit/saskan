CREATE TABLE IF NOT EXISTS SOLAR_CALENDAR_X_WEEK_TIME (
solar_calendar_x_week_time_uid_pk TEXT DEFAULT '',
solar_calendar_uid_fk TEXT DEFAULT '',
week_time_uid_fk TEXT DEFAULT '',
FOREIGN KEY (solar_calendar_uid_fk) REFERENCES SOLAR_CALENDAR(solar_calendar_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (week_time_uid_fk) REFERENCES WEEK_TIME(week_time_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (solar_calendar_x_week_time_uid_pk));
