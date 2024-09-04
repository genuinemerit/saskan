INSERT INTO LUNAR_CALENDAR (
lunar_calendar_uid_pk,
lunar_year_uid_fk,
year_name_gloss_common_uid_fk,
lunar_calendar_id,
lunar_calendar_desc,
version_id,
epoch_start_offset,
days_in_month) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
