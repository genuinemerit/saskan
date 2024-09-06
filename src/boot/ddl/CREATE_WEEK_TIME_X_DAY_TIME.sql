CREATE TABLE IF NOT EXISTS WEEK_TIME_X_DAY_TIME (
week_time_x_day_time_uid_pk TEXT DEFAULT '',
week_time_uid_fk TEXT DEFAULT '',
day_time_uid_fk TEXT DEFAULT '',
FOREIGN KEY (week_time_uid_fk) REFERENCES WEEK_TIME(week_time_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (day_time_uid_fk) REFERENCES DAY_TIME(day_time_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (week_time_x_day_time_uid_pk));
