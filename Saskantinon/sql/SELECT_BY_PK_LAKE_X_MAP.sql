SELECT lake_x_map_pk, lake_uid_fk, map_uid_fk
FROM LAKE_X_MAP
WHERE lake_x_map_pk=?
ORDER BY lake_uid_fk ASC, map_uid_fk ASC;
