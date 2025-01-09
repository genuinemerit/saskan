UPDATE `LAND_BODY_X_OCEAN_BODY` SET
`land_body_uid_fk`=?,
`ocean_body_uid_fk`=?,
`land_ocean_relation_type`=?,
`touch_type`=?,
`delete_dt`=?
WHERE `land_body_x_ocean_body_uid_pk`=?;
