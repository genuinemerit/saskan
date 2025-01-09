SELECT `gloss_common_uid_pk`,
`dialect_uid_fk`,
`gloss_type`,
`gloss_name`,
`gloss_value`,
`gloss_uri`,
`delete_dt`
FROM `GLOSS_COMMON`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `gloss_name` ASC;
