CREATE TABLE IF NOT EXISTS OCEAN_BODY_X_MAP (
ocean_body_x_map_uid_pk TEXT DEFAULT '',
ocean_body_uid_fk TEXT DEFAULT '',
map_uid_fk TEXT DEFAULT '',
FOREIGN KEY (ocean_body_uid_fk) REFERENCES OCEAN_BODY(ocean_body_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (map_uid_fk) REFERENCES MAP(map_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (ocean_body_x_map_uid_pk));