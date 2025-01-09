UPDATE `MAP_SPHERE` SET
`map_shape`=?,
`map_type`=?,
`map_name`=?,
`map_desc`=?,
`origin_lat`=?,
`origin_lon`=?,
`z_value`=?,
`unit_of_measure`=?,
`sphere_radius`=?,
`delete_dt`=?
WHERE `map_sphere_uid_pk`=?;
