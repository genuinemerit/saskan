SELECT grid_info_uid_pk, grid_cell_uid_fk, grid_info_id, grid_info_data_type, grid_info_name, grid_info_value, delete_dt
FROM GRID_INFO
WHERE g=? AND r=? AND i=? AND d=? AND _=? AND i=? AND n=? AND f=? AND o=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY grid_cell_val_name ASC;
