CREATE TABLE IF NOT EXISTS MONTH (
month_uid_pk TEXT DEFAULT '',
month_name_gloss_common_uid_fk TEXT DEFAULT '',
month_id TEXT DEFAULT '',
version_id TEXT DEFAULT '',
days_in_month INTEGER DEFAULT 0,
months_number INTEGER DEFAULT 0,
is_leap_day_month BOOLEAN DEFAULT 0,
is_leap_month BOOLEAN DEFAULT 0,
delete_dt TEXT DEFAULT '',
FOREIGN KEY (month_name_gloss_common_uid_fk) REFERENCES GLOSS_COMMON(gloss_common_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (month_uid_pk));
