CREATE TABLE IF NOT EXISTS WEEK_TIME_X_DAY_TIME (
week_time_x_day_time_uid_pk TEXT DEFAULT '',
week_time_uid_fk TEXT DEFAULT '',
day_time_uid_fk TEXT DEFAULT '',
touch_type TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (touch_type IN ('contains', 'is_contained_by', 'borders', 'overlaps', 'informs', 'layers_above', 'layers_below')),
FOREIGN KEY (week_time_uid_fk) REFERENCES WEEK_TIME(week_time_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (day_time_uid_fk) REFERENCES DAY_TIME(day_time_uid_pk) ON DELETE CASCADE,PRIMARY KEY (week_time_x_day_time_uid_pk));
