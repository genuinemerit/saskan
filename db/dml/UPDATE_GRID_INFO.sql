UPDATE `GRID_INFO` SET
`grid_uid_fk`=?,
`grid_cell_uid_fk`=?,
`grid_id`=?,
`grid_cell_name`=?,
`grid_info_id`=?,
`lang_code`=?,
`grid_info_name`=?,
`grid_info_int`=?,
`grid_info_float`=?,
`grid_info_str`=?,
`grid_info_json`=?,
`grid_info_img_path`=?,
`grid_info_img`=?,
`delete_dt`=?
WHERE `grid_info_uid_pk`=?;
