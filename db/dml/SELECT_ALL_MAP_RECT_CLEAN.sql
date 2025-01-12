SELECT `map_rect_uid_pk`,
`map_shape`,
`map_type`,
`map_id`,
`lang_code`,
`map_name`,
`map_desc`,
`north_lat`,
`south_lat`,
`east_lon`,
`west_lon`,
`delete_dt`
FROM `MAP_RECT`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `map_name` ASC;
