SELECT `solar_year_uid_pk`,
`world_uid_fk`,
`lang_uid_fk`,
`solar_year_key`,
`version_id`,
`solar_year_name`,
`solar_year_desc`,
`solar_year_span`,
`days_in_solar_year`,
`delete_dt`
FROM `SOLAR_YEAR`
ORDER BY `solar_year_key` ASC;
