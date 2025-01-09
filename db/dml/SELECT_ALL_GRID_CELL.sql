SELECT `grid_cell_uid_pk`,
`grid_uid_fk`,
`grid_name`,
`grid_cell_name`,
`x_col_ix`,
`y_row_ix`,
`z_up_down_ix`,
`grid_cell_id`,
`delete_dt`
FROM `GRID_CELL`
ORDER BY `grid_cell_name` ASC;
