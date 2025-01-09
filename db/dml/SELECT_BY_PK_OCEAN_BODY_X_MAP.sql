SELECT `ocean_body_x_map_uid_pk`, `ocean_body_uid_fk`, `map_uid_fk`, `touch_type`, `delete_dt`
FROM `OCEAN_BODY_X_MAP`
WHERE `ocean_body_x_map_uid_pk` = ?
ORDER BY `ocean_body_x_map_uid_pk ASC`;
