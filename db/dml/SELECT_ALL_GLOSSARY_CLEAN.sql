SELECT `glossary_uid_pk`,
`gloss_common_uid_fk`,
`dialect_uid_fk`,
`gloss_type`,
`gloss_name`,
`gloss_value`,
`gloss_uri`,
`delete_dt`
FROM `GLOSSARY`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `gloss_name` ASC;
