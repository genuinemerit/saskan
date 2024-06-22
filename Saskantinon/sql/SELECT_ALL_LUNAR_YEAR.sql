SELECT lunar_year_uid_pk,
world_uid_fk,
lang_uid_fk,
lunar_year_key,
version_id,
lunar_year_name,
lunar_year_desc,
days_in_lunar_year
FROM LUNAR_YEAR
ORDER BY lunar_year_key ASC, version_id ASC;
