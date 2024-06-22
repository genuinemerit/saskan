CREATE TABLE IF NOT EXISTS LAND_BODY (
land_body_uid_pk TEXT DEFAULT '',
gloss_common_uid_fk TEXT DEFAULT '',
body_landline_points_json TEXT DEFAULT '',
land_body_type TEXT DEFAULT '',
land_body_surface_area_m2 NUMERIC DEFAULT 0.0,
land_body_surface_avg_altitude_m NUMERIC DEFAULT 0.0,
max_altitude_m NUMERIC DEFAULT 0.0,
min_altitude_m NUMERIC DEFAULT 0.0,
CHECK (land_body_type IN ('island', 'continent', 'sub-continent', 'region')),
FOREIGN KEY (gloss_common_uid_fk) REFERENCES GLOSS_COMMON(gloss_common_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (land_body_uid_pk));
