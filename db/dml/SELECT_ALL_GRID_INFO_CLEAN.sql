SELECT `grid_info_uid_pk`,
`grid_uid_fk`,
`grid_cell_uid_fk`,
`grid_name`,
`grid_cell_name`,
`grid_info_id`,
`grid_info_data_type`,
`grid_info_name`,
`grid_info_value`,
`grid_info_path`,
`delete_dt`
FROM `GRID_INFO`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `grid_info_name` ASC;
