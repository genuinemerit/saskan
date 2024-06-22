CREATE TABLE IF NOT EXISTS DAY_TIME (
day_time_uid_pk TEXT DEFAULT '',
day_time_name_gloss_common_uid_fk TEXT DEFAULT '',
day_time_desc TEXT DEFAULT '',
day_time_id TEXT DEFAULT '',
version_id TEXT DEFAULT '',
hours_in_day_time INTEGER DEFAULT 0,
day_time_number INTEGER DEFAULT 0,
is_leap_day_time BOOLEAN DEFAULT 0,
FOREIGN KEY (day_time_name_gloss_common_uid_fk) REFERENCES GLOSS_COMMON(gloss_common_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (day_time_uid_pk));
