SELECT grid_uid_pk, version_id, grid_name, row_cnt, col_cnt, z_up_cnt, z_down_cnt
FROM GRID
WHERE grid_uid_pk=?
ORDER BY grid_name ASC;
