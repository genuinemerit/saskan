UPDATE `SEASON` SET
`solar_year_uid_fk`=?,
`gloss_common_uid_vfk`=?,
`season_type`=?,
`hemisphere_type`=?,
`years_in_season`=?,
`delete_dt`=?
WHERE `season_uid_pk`=?;
