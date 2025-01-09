UPDATE `WEEK_TIME` SET
`week_time_name_gloss_common_uid_vfk`=?,
`week_time_name`=?,
`week_time_desc`=?,
`days_in_week_time`=?,
`week_time_order`=?,
`is_leap_week_time`=?,
`delete_dt`=?
WHERE `week_time_uid_pk`=?;
