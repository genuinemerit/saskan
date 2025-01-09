SELECT `grid_x_map_uid_pk`,
`grid_uid_fk`,
`map_uid_vfk`,
`delete_dt`
FROM `GRID_X_MAP`
WHERE delete_dt IS NULL OR delete_dt = '';
