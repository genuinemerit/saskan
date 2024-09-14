SELECT map_rect_uid_pk, map_shape, map_type, map_name, map_desc, north_lat, south_lat, east_lon, west_lon, delete_dt
FROM MAP_RECT
WHERE m=? AND a=? AND p=? AND _=? AND r=? AND e=? AND c=? AND t=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY map_name ASC;
