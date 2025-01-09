CREATE TABLE IF NOT EXISTS DAY_TIME (
day_time_uid_pk TEXT DEFAULT '',
day_time_name_gloss_common_uid_vfk TEXT DEFAULT '',
day_time_name TEXT DEFAULT '',
day_time_desc TEXT DEFAULT '',
hours_in_day_time INTEGER DEFAULT 0,
day_time_number INTEGER DEFAULT 0,
is_leap_day_time BOOLEAN DEFAULT 0,
delete_dt TEXT DEFAULT '',
PRIMARY KEY (day_time_uid_pk));
