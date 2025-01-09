SELECT `solar_calendar_x_moon_uid_pk`,
`solar_calendar_uid_fk`,
`month_uid_fk`,
`touch_type`,
`delete_dt`
FROM `SOLAR_CALENDAR_X_MONTH`
WHERE delete_dt IS NULL OR delete_dt = '';
