CREATE TABLE IF NOT EXISTS LUNAR_CALENDAR_X_WEEK_TIME (
lunar_calendar_x_week_time_uid_pk TEXT DEFAULT '',
lunar_calendar_uid_fk TEXT DEFAULT '',
week_time_uid_fk TEXT DEFAULT '',
FOREIGN KEY (lunar_calendar_uid_fk) REFERENCES LUNAR_CALENDAR(lunar_calendar_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (week_time_uid_fk) REFERENCES WEEK_TIME(week_time_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (lunar_calendar_x_week_time_uid_pk));
