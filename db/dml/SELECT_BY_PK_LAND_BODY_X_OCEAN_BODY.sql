SELECT `land_body_x_ocean_body_uid_pk`, `land_body_uid_fk`, `ocean_body_uid_fk`, `land_ocean_relation_type`, `touch_type`, `delete_dt`
FROM `LAND_BODY_X_OCEAN_BODY`
WHERE `land_body_x_ocean_body_uid_pk` = ?
ORDER BY `land_body_x_ocean_body_uid_pk ASC`;