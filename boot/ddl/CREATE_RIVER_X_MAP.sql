CREATE TABLE IF NOT EXISTS RIVER_X_MAP (
river_x_map_uid_pk TEXT DEFAULT '',
river_uid_fk TEXT DEFAULT '',
map_uid_fk TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
FOREIGN KEY (river_uid_fk) REFERENCES RIVER(river_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (map_uid_fk) REFERENCES MAP(map_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (river_x_map_uid_pk));
