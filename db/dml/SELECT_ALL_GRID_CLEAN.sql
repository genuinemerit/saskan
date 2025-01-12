SELECT `grid_uid_pk`,
`grid_id`,
`x_col_cnt`,
`y_row_cnt`,
`z_up_cnt`,
`z_down_cnt`,
`delete_dt`
FROM `GRID`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `grid_id` ASC;
