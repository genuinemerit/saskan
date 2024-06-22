CREATE TABLE IF NOT EXISTS LAND_BODY_X_OCEAN_BODY (
land_body_x_ocean_body_uid_pk TEXT DEFAULT '',
land_body_uid_fk TEXT DEFAULT '',
ocean_body_uid_fk TEXT DEFAULT '',
land_ocean_relation_type TEXT DEFAULT '',
CHECK (land_ocean_relation_type IN ('borders', 'overlaps', 'contains', 'contained by')),
FOREIGN KEY (land_body_uid_fk) REFERENCES LAND_BODY(land_body_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (ocean_body_uid_fk) REFERENCES OCEAN_BODY(ocean_body_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (land_body_x_ocean_body_uid_pk));
