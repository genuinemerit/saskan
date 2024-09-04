SELECT solar_year_uid_pk, world_uid_fk, lang_uid_fk, solar_year_key, version_id, solar_year_name, solar_year_desc, days_in_solar_year
FROM SOLAR_YEAR
WHERE solar_year_uid_pk=?
ORDER BY solar_year_key ASC, version_id ASC;
