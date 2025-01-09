SELECT `dialect_uid_pk`,
`lang_uid_fk`,
`dialect_name`,
`dialect_desc`,
`divergence_factors`,
`syncretic_factors`,
`preservation_factors`,
`delete_dt`
FROM `LANG_DIALECT`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `dialect_name` ASC;
