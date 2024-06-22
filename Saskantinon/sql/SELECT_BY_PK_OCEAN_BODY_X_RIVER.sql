SELECT ocean_body_x_river_uid_pk, ocean_body_uid_fk, river_uid_fk
FROM OCEAN_BODY_X_RIVER
WHERE ocean_body_x_river_uid_pk=?
ORDER BY ocean_body_x_river_uid_pk ASC;
