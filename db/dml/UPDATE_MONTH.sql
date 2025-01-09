UPDATE `MONTH` SET
`month_name_gloss_common_uid_vfk`=?,
`month_name`=?,
`days_in_month`=?,
`month_order`=?,
`is_leap_day_month`=?,
`is_leap_month`=?,
`delete_dt`=?
WHERE `month_uid_pk`=?;
