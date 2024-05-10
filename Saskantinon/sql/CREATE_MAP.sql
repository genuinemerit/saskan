CREATE TABLE IF NOT EXISTS MAP (
map_uid_pk TEXT DEFAULT '',
map_name TEXT DEFAULT '',
map_type TEXT DEFAULT '',
-- GROUP geo_map_loc: <class 'io_data.Struct.GameGeoLocation'>
geo_map_loc_latitude_north_dg NUMERIC DEFAULT 0.0,
geo_map_loc_latitude_south_dg NUMERIC DEFAULT 0.0,
geo_map_loc_longitude_east_dg NUMERIC DEFAULT 0.0,
geo_map_loc_longitude_west_dg NUMERIC DEFAULT 0.0,
geo_map_loc_avg_altitude_m NUMERIC DEFAULT 0.0,
geo_map_loc_max_altitude_m NUMERIC DEFAULT 0.0,
geo_map_loc_min_altitude_m NUMERIC DEFAULT 0.0,
-- GROUP three_d_map_loc: <class 'io_data.Struct.Game3DLocation'>
three_d_map_loc_origin_x NUMERIC DEFAULT 0.0,
three_d_map_loc_origin_y NUMERIC DEFAULT 0.0,
three_d_map_loc_origin_z NUMERIC DEFAULT 0.0,
three_d_map_loc_width_x NUMERIC DEFAULT 0.0,
three_d_map_loc_height_y NUMERIC DEFAULT 0.0,
three_d_map_loc_depth_z NUMERIC DEFAULT 0.0,
CHECK (map_type IN ('geo', 'astro', 'underwater', 'underground', 'informational', 'political')),
PRIMARY KEY (map_uid_pk));
