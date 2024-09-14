SELECT month_uid_pk, month_name_gloss_common_uid_fk, month_id, version_id, days_in_month, months_number, is_leap_day_month, is_leap_month, delete_dt
FROM MONTH
WHERE m=? AND o=? AND n=? AND t=? AND h=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY month_id ASC, version_id ASC;
