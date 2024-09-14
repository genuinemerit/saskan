SELECT lunar_year_uid_pk, world_uid_fk, lang_uid_fk, lunar_year_key, version_id, lunar_year_name, lunar_year_desc, days_in_lunar_year, delete_dt
FROM LUNAR_YEAR
WHERE l=? AND u=? AND n=? AND a=? AND r=? AND _=? AND y=? AND e=? AND a=? AND r=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY lunar_year_key ASC, version_id ASC;
