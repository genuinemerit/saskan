SELECT `lake_x_map_pk`,
`lake_uid_fk`,
`map_uid_fk`,
`touch_type`,
`delete_dt`
FROM `LAKE_X_MAP`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `lake_uid_fk` ASC, `map_uid_fk` ASC;
