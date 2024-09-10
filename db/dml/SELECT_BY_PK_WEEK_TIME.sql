SELECT week_time_uid_pk, week_time_name_gloss_common_uid_fk, week_time_desc, week_time_id, version_id, days_in_week_time, week_time_number, is_leap_week_time, delete_dt
FROM WEEK_TIME
WHERE week_time_uid_pk=?
ORDER BY week_time_id ASC, version_id ASC;
