SELECT `river_x_map_uid_pk`,
`river_uid_fk`,
`map_uid_fk`,
`touch_type`,
`delete_dt`
FROM `RIVER_X_MAP`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `river_x_map_uid_pk` ASC;
