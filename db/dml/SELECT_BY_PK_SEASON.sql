SELECT season_uid_pk, solar_year_uid_fk, gloss_common_uid_fk, version_id, season_type, hemisphere_type, years_in_season, delete_dt
FROM SEASON
WHERE s=? AND e=? AND a=? AND s=? AND o=? AND n=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY season_uid_pk ASC, season_type ASC;
