SELECT `map_sphere_uid_pk`, `map_shape`, `map_type`, `map_id`, `lang_code`, `map_name`, `map_desc`, `origin_lat`, `origin_lon`, `z_value`, `unit_of_measure`, `sphere_radius`, `delete_dt`
FROM `MAP_SPHERE`
WHERE `map_sphere_uid_pk` = ?
ORDER BY `map_name ASC`;
