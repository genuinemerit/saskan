UPDATE MAP SET
map_name=?,
map_type=?,
geo_map_loc_latitude_north_dg=?,
geo_map_loc_latitude_south_dg=?,
geo_map_loc_longitude_east_dg=?,
geo_map_loc_longitude_west_dg=?,
geo_map_loc_avg_altitude_m=?,
geo_map_loc_max_altitude_m=?,
geo_map_loc_min_altitude_m=?,
three_d_map_loc_origin_x=?,
three_d_map_loc_origin_y=?,
three_d_map_loc_origin_z=?,
three_d_map_loc_width_x=?,
three_d_map_loc_height_y=?,
three_d_map_loc_depth_z=?
WHERE map_uid_pk=?;
