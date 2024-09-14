SELECT grid_uid_pk, grid_name, x_col_cnt, y_row_cnt, z_up_cnt, z_down_cnt, delete_dt
FROM GRID
WHERE g=? AND r=? AND i=? AND d=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY grid_name ASC;
