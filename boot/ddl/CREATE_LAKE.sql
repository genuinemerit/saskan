CREATE TABLE IF NOT EXISTS LAKE (
lake_uid_pk TEXT DEFAULT '',
gloss_common_uid_vfk TEXT DEFAULT '',
lake_name TEXT DEFAULT '',
lake_shoreline_points_json JSON DEFAULT '',
lake_size TEXT DEFAULT 'medium',
water_type TEXT DEFAULT 'freshwater',
lake_type TEXT DEFAULT 'lake',
is_tidal_influence BOOLEAN DEFAULT 0,
lake_surface_m2 NUMERIC DEFAULT 0.0,
max_depth_m NUMERIC DEFAULT 0.0,
avg_depth_m NUMERIC DEFAULT 0.0,
lake_altitude_m NUMERIC DEFAULT 0.0,
catchment_area_radius_m NUMERIC DEFAULT 0.0,
lake_origin TEXT DEFAULT '',
flora_and_fauna TEXT DEFAULT '',
water_color TEXT DEFAULT '',
accessibility TEXT DEFAULT '',
special_features TEXT DEFAULT '',
lake_usage TEXT DEFAULT '',
lake_lore TEXT DEFAULT '',
lake_history TEXT DEFAULT '',
conservation_status TEXT DEFAULT '',
current_conditions TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (lake_size IN ('small', 'medium', 'large')),
CHECK (water_type IN ('freshwater', 'saline', 'brackish')),
CHECK (lake_type IN ('lake', 'reservoir', 'pond', 'pool', 'loch', 'hot spring', 'swamp', 'marsh', 'mill pond', 'oxbow lake', 'spring', 'sinkhole', 'acquifer', 'vernal pool', 'wadi')),
PRIMARY KEY (lake_uid_pk));
