SELECT `season_uid_pk`,
`solar_year_uid_fk`,
`gloss_common_uid_vfk`,
`season_type`,
`hemisphere_type`,
`years_in_season`,
`delete_dt`
FROM `SEASON`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `season_uid_pk` ASC, `season_type` ASC;
