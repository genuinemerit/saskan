SELECT grid_info_uid_pk,
grid_cell_uid_fk,
grid_info_id,
grid_info_data_type,
grid_info_name,
grid_info_value,
delete_dt
FROM GRID_INFO
ORDER BY grid_info_name ASC;
