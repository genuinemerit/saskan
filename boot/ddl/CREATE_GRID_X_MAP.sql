CREATE TABLE IF NOT EXISTS GRID_X_MAP (
grid_x_map_uid_pk TEXT DEFAULT '',
grid_uid_fk TEXT DEFAULT '',
map_uid_fk TEXT DEFAULT '',
FOREIGN KEY (grid_uid_fk) REFERENCES GRID(grid_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (map_uid_fk) REFERENCES MAP(map_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (grid_x_map_uid_pk));
