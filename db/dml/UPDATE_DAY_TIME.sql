UPDATE `DAY_TIME` SET
`day_time_name_gloss_common_uid_vfk`=?,
`day_time_name`=?,
`day_time_desc`=?,
`hours_in_day_time`=?,
`day_time_number`=?,
`is_leap_day_time`=?,
`delete_dt`=?
WHERE `day_time_uid_pk`=?;
