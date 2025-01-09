SELECT `land_body_x_land_body_uid_pk`, `land_body_1_uid_fk`, `land_body_2_uid_fk`, `land_land_relation_type`, `touch_type`, `delete_dt`
FROM `LAND_BODY_X_LAND_BODY`
WHERE `land_body_x_land_body_uid_pk` = ?
ORDER BY `land_body_x_land_body_uid_pk ASC`;
