CREATE TABLE IF NOT EXISTS _MAP (
CHECK (map_shape IN ('rectangle', 'box', 'sphere')),
CHECK (map_type IN ('geo', 'astro', 'underwater', 'underground', 'info', 'political')),
PRIMARY KEY (map_uid_pk));
