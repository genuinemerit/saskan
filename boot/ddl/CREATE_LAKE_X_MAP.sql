CREATE TABLE IF NOT EXISTS LAKE_X_MAP (
lake_x_map_pk TEXT DEFAULT '',
lake_uid_fk TEXT DEFAULT '',
map_uid_fk TEXT DEFAULT '',
touch_type TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (touch_type IN ('contains', 'is_contained_by', 'borders', 'overlaps', 'informs', 'layers_above', 'layers_below')),
FOREIGN KEY (lake_uid_fk) REFERENCES LAKE(lake_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (map_uid_fk) REFERENCES MAP(map_uid_pk) ON DELETE CASCADE,PRIMARY KEY (lake_x_map_pk));
