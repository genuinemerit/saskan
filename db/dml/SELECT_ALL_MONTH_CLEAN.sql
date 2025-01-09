SELECT `month_uid_pk`,
`month_name_gloss_common_uid_vfk`,
`month_name`,
`days_in_month`,
`month_order`,
`is_leap_day_month`,
`is_leap_month`,
`delete_dt`
FROM `MONTH`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `month_id` ASC;
