SELECT `ocean_body_x_map_uid_pk`,
`ocean_body_uid_fk`,
`map_uid_fk`,
`touch_type`,
`delete_dt`
FROM `OCEAN_BODY_X_MAP`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `ocean_body_x_map_uid_pk` ASC;
