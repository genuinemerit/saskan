CREATE TABLE IF NOT EXISTS LAND_BODY_X_MAP (
land_body_x_map_uid_pk TEXT DEFAULT '',
land_body_uid_fk TEXT DEFAULT '',
map_uid_fk TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
FOREIGN KEY (land_body_uid_fk) REFERENCES LAND_BODY(land_body_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (map_uid_fk) REFERENCES MAP(map_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (land_body_x_map_uid_pk));
