CREATE TABLE IF NOT EXISTS MAP_RECT (
map_rect_uid_pk TEXT DEFAULT '',
map_shape TEXT DEFAULT '',
map_type TEXT DEFAULT '',
map_name TEXT DEFAULT '',
map_desc TEXT DEFAULT '',
north_lat NUMERIC DEFAULT 0.0,
south_lat NUMERIC DEFAULT 0.0,
east_lon NUMERIC DEFAULT 0.0,
west_lon NUMERIC DEFAULT 0.0,
delete_dt TEXT DEFAULT '',
CHECK (map_shape IN ('rectangle', 'box', 'sphere')),
CHECK (map_type IN ('geo', 'astro', 'underwater', 'underground', 'info', 'political')),
PRIMARY KEY (map_rect_uid_pk));
