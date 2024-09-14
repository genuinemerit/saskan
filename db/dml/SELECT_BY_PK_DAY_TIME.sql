SELECT day_time_uid_pk, day_time_name_gloss_common_uid_fk, day_time_desc, day_time_id, version_id, hours_in_day_time, day_time_number, is_leap_day_time, delete_dt
FROM DAY_TIME
WHERE d=? AND a=? AND y=? AND _=? AND t=? AND i=? AND m=? AND e=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY day_time_id ASC, version_id ASC;
