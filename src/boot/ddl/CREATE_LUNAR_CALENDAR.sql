CREATE TABLE IF NOT EXISTS LUNAR_CALENDAR (
lunar_calendar_uid_pk TEXT DEFAULT '',
lunar_year_uid_fk TEXT DEFAULT '',
year_name_gloss_common_uid_fk TEXT DEFAULT '',
lunar_calendar_id TEXT DEFAULT '',
lunar_calendar_desc TEXT DEFAULT '',
version_id TEXT DEFAULT '',
epoch_start_offset INTEGER DEFAULT 0,
days_in_month INTEGER DEFAULT 0,
FOREIGN KEY (lunar_year_uid_fk) REFERENCES LUNAR_YEAR(lunar_year_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (year_name_gloss_common_uid_fk) REFERENCES GLOSS_COMMON(gloss_common_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (lunar_calendar_uid_pk));
