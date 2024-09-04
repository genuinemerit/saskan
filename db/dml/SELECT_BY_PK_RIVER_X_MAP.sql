SELECT river_x_map_uid_pk, river_uid_fk, map_uid_fk
FROM RIVER_X_MAP
WHERE river_x_map_uid_pk=?
ORDER BY river_x_map_uid_pk ASC;
