SELECT `week_time_x_day_time_uid_pk`,
`week_time_uid_fk`,
`day_time_uid_fk`,
`touch_type`,
`delete_dt`
FROM `WEEK_TIME_X_DAY_TIME`
WHERE delete_dt IS NULL OR delete_dt = '';
