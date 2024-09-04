SELECT day_time_uid_pk,
day_time_name_gloss_common_uid_fk,
day_time_desc,
day_time_id,
version_id,
hours_in_day_time,
day_time_number,
is_leap_day_time
FROM DAY_TIME
ORDER BY day_time_id ASC, version_id ASC;
