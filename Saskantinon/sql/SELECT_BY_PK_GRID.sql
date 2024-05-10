SELECT grid_uid_pk, grid_name, row_cnt, col_cnt, z_up_cnt, z_down_cnt, width_px, height_px, width_km, height_km, z_up_m, z_down_m
FROM GRID
WHERE grid_uid_pk=?
ORDER BY grid_name ASC;
