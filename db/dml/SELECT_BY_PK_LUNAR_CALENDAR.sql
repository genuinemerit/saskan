SELECT lunar_calendar_uid_pk, lunar_year_uid_fk, year_name_gloss_common_uid_fk, lunar_calendar_id, lunar_calendar_desc, version_id, epoch_start_offset, days_in_month, delete_dt
FROM LUNAR_CALENDAR
WHERE lunar_calendar_uid_pk=?
ORDER BY lunar_calendar_id ASC, version_id ASC;
