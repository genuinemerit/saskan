CREATE TABLE IF NOT EXISTS MONTH (
month_uid_pk TEXT DEFAULT '',
month_name_gloss_common_uid_vfk TEXT DEFAULT '',
month_name TEXT DEFAULT '',
days_in_month INTEGER DEFAULT 0,
month_order INTEGER DEFAULT 0,
is_leap_day_month BOOLEAN DEFAULT 0,
is_leap_month BOOLEAN DEFAULT 0,
delete_dt TEXT DEFAULT '',
PRIMARY KEY (month_uid_pk));
