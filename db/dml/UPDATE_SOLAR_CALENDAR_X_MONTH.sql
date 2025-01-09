UPDATE `SOLAR_CALENDAR_X_MONTH` SET
`solar_calendar_uid_fk`=?,
`month_uid_fk`=?,
`touch_type`=?,
`delete_dt`=?
WHERE `solar_calendar_x_moon_uid_pk`=?;
