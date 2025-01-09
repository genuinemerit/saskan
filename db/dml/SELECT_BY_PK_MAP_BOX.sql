SELECT `map_box_uid_pk`, `map_shape`, `map_type`, `map_name`, `map_desc`, `north_lat`, `south_lat`, `east_lon`, `west_lon`, `up_m`, `down_m`, `delete_dt`
FROM `MAP_BOX`
WHERE `map_box_uid_pk` = ?
ORDER BY `map_name ASC`;
