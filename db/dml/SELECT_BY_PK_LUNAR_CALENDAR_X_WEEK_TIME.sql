SELECT lunar_calendar_x_week_time_uid_pk, lunar_calendar_uid_fk, week_time_uid_fk, delete_dt
FROM LUNAR_CALENDAR_X_WEEK_TIME
WHERE lunar_calendar_x_week_time_uid_pk=?;
