SELECT lunar_calendar_uid_pk, lunar_year_uid_fk, year_name_gloss_common_uid_fk, lunar_calendar_id, lunar_calendar_desc, version_id, epoch_start_offset, days_in_month, delete_dt
FROM LUNAR_CALENDAR
WHERE l=? AND u=? AND n=? AND a=? AND r=? AND _=? AND c=? AND a=? AND l=? AND e=? AND n=? AND d=? AND a=? AND r=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY lunar_calendar_id ASC, version_id ASC;
