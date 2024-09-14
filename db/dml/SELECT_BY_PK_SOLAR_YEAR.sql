SELECT solar_year_uid_pk, world_uid_fk, lang_uid_fk, solar_year_key, version_id, solar_year_name, solar_year_desc, days_in_solar_year, delete_dt
FROM SOLAR_YEAR
WHERE s=? AND o=? AND l=? AND a=? AND r=? AND _=? AND y=? AND e=? AND a=? AND r=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY solar_year_key ASC, version_id ASC;
