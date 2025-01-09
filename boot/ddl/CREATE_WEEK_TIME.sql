CREATE TABLE IF NOT EXISTS WEEK_TIME (
week_time_uid_pk TEXT DEFAULT '',
week_time_name_gloss_common_uid_vfk TEXT DEFAULT '',
week_time_name TEXT DEFAULT '',
week_time_desc TEXT DEFAULT '',
days_in_week_time INTEGER DEFAULT 0,
week_time_order INTEGER DEFAULT 0,
is_leap_week_time BOOLEAN DEFAULT 0,
delete_dt TEXT DEFAULT '',
PRIMARY KEY (week_time_uid_pk));
