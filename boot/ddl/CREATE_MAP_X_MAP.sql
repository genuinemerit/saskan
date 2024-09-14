CREATE TABLE IF NOT EXISTS MAP_X_MAP (
map_x_map_uid_pk TEXT DEFAULT '',
map_uid_1_fk TEXT DEFAULT '',
map_uid_2_fk TEXT DEFAULT '',
touch_type TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (touch_type IN ('contains', 'is_contained_by', 'borders', 'overlaps', 'informs', 'layers_above', 'layers_below')),
PRIMARY KEY (map_x_map_uid_pk));
