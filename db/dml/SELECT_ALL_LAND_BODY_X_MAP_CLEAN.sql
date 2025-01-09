SELECT `land_body_x_map_uid_pk`,
`land_body_uid_fk`,
`map_uid_fk`,
`touch_type`,
`delete_dt`
FROM `LAND_BODY_X_MAP`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `land_body_x_map_uid_pk` ASC;
