SELECT `lunar_year_uid_pk`, `world_uid_fk`, `lang_uid_vfk`, `lunar_year_name`, `lunar_year_desc`, `days_in_lunar_year`, `delete_dt`
FROM `LUNAR_YEAR`
WHERE `lunar_year_uid_pk` = ?
ORDER BY `lunar_year_key ASC`;
