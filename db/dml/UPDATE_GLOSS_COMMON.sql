UPDATE `GLOSS_COMMON` SET
`dialect_uid_fk`=?,
`gloss_type`=?,
`gloss_name`=?,
`gloss_value`=?,
`gloss_uri`=?,
`delete_dt`=?
WHERE `gloss_common_uid_pk`=?;
