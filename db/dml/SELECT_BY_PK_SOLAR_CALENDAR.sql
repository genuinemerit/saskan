SELECT `solar_calendar_uid_pk`, `solar_year_uid_fk`, `year_name_gloss_common_uid_vfk`, `season_start_uid_fk`, `solar_calendar_name`, `solar_calendar_desc`, `epoch_start_offset`, `months_in_year`, `watches_in_day`, `hours_in_watch`, `minutes_in_hour`, `seconds_in_minute`, `leap_year`, `leap_month`, `leap_days`, `leap_rule`, `delete_dt`
FROM `SOLAR_CALENDAR`
WHERE `solar_calendar_uid_pk` = ?
ORDER BY `solar_calendar_id ASC`;
