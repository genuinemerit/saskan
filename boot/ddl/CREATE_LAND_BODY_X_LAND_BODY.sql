CREATE TABLE IF NOT EXISTS LAND_BODY_X_LAND_BODY (
land_body_x_land_body_uid_pk TEXT DEFAULT '',
land_body_1_uid_fk TEXT DEFAULT '',
land_body_2_uid_fk TEXT DEFAULT '',
land_land_relation_type TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (land_land_relation_type IN ('borders', 'overlaps', 'contains', 'contained by')),
FOREIGN KEY (land_body_1_uid_fk) REFERENCES LAND_BODY(land_body_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (land_body_2_uid_fk) REFERENCES LAND_BODY(land_body_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (land_body_x_land_body_uid_pk));
