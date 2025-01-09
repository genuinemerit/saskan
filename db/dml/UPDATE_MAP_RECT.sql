UPDATE `MAP_RECT` SET
`map_shape`=?,
`map_type`=?,
`map_name`=?,
`map_desc`=?,
`north_lat`=?,
`south_lat`=?,
`east_lon`=?,
`west_lon`=?,
`delete_dt`=?
WHERE `map_rect_uid_pk`=?;
