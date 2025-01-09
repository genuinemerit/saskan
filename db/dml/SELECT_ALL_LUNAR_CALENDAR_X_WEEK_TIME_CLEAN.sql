SELECT `lunar_calendar_x_week_time_uid_pk`,
`lunar_calendar_uid_fk`,
`week_time_uid_fk`,
`touch_type`,
`delete_dt`
FROM `LUNAR_CALENDAR_X_WEEK_TIME`
WHERE delete_dt IS NULL OR delete_dt = '';
