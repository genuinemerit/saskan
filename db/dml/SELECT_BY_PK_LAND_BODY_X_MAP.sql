SELECT land_body_x_map_uid_pk, land_body_uid_fk, map_uid_fk
FROM LAND_BODY_X_MAP
WHERE land_body_x_map_uid_pk=?
ORDER BY land_body_x_map_uid_pk ASC;
