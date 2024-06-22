UPDATE SOLAR_CALENDAR SET
solar_year_uid_fk=?,
year_name_gloss_common_uid_fk=?,
season_start_uid_fk=?,
solar_calendar_id=?,
solar_calendar_desc=?,
version_id=?,
epoch_start_offset=?,
months_in_year=?,
watches_in_day=?,
hours_in_watch=?,
minutes_in_hour=?,
seconds_in_minute=?,
leap_year=?,
leap_month=?,
leap_days=?,
leap_rule=?
WHERE solar_calendar_uid_pk=?;
