SELECT `lunar_calendar_x_moon_uid_pk`, `lunar_calendar_uid_fk`, `month_uid_fk`, `touch_type`, `delete_dt`
FROM `LUNAR_CALENDAR_X_MONTH`
WHERE `lunar_calendar_x_moon_uid_pk` = ?;