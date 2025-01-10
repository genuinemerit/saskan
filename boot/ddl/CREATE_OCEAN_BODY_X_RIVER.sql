CREATE TABLE IF NOT EXISTS OCEAN_BODY_X_RIVER (
ocean_body_x_river_uid_pk TEXT DEFAULT '',
ocean_body_uid_fk TEXT DEFAULT '',
river_uid_fk TEXT DEFAULT '',
touch_type TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (touch_type IN ('contains', 'is_contained_by', 'borders', 'overlaps', 'informs', 'layers_above', 'layers_below')),
FOREIGN KEY (ocean_body_uid_fk) REFERENCES OCEAN_BODY(ocean_body_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (river_uid_fk) REFERENCES RIVER(river_uid_pk) ON DELETE CASCADE,PRIMARY KEY (ocean_body_x_river_uid_pk));