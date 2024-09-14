SELECT grid_cell_uid_pk,
grid_uid_fk,
grid_cell_name,
grid_cell_id,
x_row_ix,
y_col_ix,
z_up_down_ix,
delete_dt
FROM GRID_CELL
ORDER BY grid_name ASC;
