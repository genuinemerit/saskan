SELECT lake_x_map_pk, lake_uid_fk, map_uid_fk, delete_dt
FROM LAKE_X_MAP
WHERE l=? AND a=? AND k=? AND e=? AND _=? AND x=? AND _=? AND m=? AND a=? AND p=? AND _=? AND p=? AND k=?
ORDER BY lake_uid_fk ASC, map_uid_fk ASC;
