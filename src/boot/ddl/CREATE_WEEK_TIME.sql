CREATE TABLE IF NOT EXISTS WEEK_TIME (
week_time_uid_pk TEXT DEFAULT '',
week_time_name_gloss_common_uid_fk TEXT DEFAULT '',
week_time_desc TEXT DEFAULT '',
week_time_id TEXT DEFAULT '',
version_id TEXT DEFAULT '',
days_in_week_time INTEGER DEFAULT 0,
week_time_number INTEGER DEFAULT 0,
is_leap_week_time BOOLEAN DEFAULT 0,
FOREIGN KEY (week_time_name_gloss_common_uid_fk) REFERENCES GLOSS_COMMON(gloss_common_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (week_time_uid_pk));
