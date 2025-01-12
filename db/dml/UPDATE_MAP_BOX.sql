UPDATE `MAP_BOX` SET
`map_shape`=?,
`map_type`=?,
`map_id`=?,
`lang_code`=?,
`map_name`=?,
`map_desc`=?,
`north_lat`=?,
`south_lat`=?,
`east_lon`=?,
`west_lon`=?,
`up_m`=?,
`down_m`=?,
`delete_dt`=?
WHERE `map_box_uid_pk`=?;
