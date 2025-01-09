UPDATE `SOLAR_CALENDAR_X_WEEK_TIME` SET
`solar_calendar_uid_fk`=?,
`week_time_uid_fk`=?,
`touch_type`=?,
`delete_dt`=?
WHERE `solar_calendar_x_week_time_uid_pk`=?;
