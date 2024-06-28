SELECT season_uid_pk, solar_year_uid_fk, gloss_common_uid_fk, version_id, season_type, hemisphere_type, years_in_season
FROM SEASON
WHERE season_uid_pk=?
ORDER BY season_uid_pk ASC, season_type ASC;