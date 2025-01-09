SELECT `day_time_uid_pk`,
`day_time_name_gloss_common_uid_vfk`,
`day_time_name`,
`day_time_desc`,
`hours_in_day_time`,
`day_time_number`,
`is_leap_day_time`,
`delete_dt`
FROM `DAY_TIME`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `day_time_id` ASC;
