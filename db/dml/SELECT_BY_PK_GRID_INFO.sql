SELECT `grid_info_uid_pk`, `grid_uid_fk`, `grid_cell_uid_fk`, `grid_name`, `grid_cell_name`, `grid_info_id`, `grid_info_name`, `grid_info_int`, `grid_info_float`, `grid_info_str`, `grid_info_json`, `grid_info_img_path`, `grid_info_img`, `delete_dt`
FROM `GRID_INFO`
WHERE `grid_info_uid_pk` = ?
ORDER BY `grid_info_name ASC`;
