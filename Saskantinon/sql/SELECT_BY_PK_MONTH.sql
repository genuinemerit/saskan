SELECT month_uid_pk, month_name_gloss_common_uid_fk, month_id, version_id, days_in_month, months_number, is_leap_day_month, is_leap_month
FROM MONTH
WHERE month_uid_pk=?
ORDER BY month_id ASC, version_id ASC;
