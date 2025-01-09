SELECT `char_set_uid_pk`,
`font_name`,
`char_set_type`,
`char_set_desc`,
`delete_dt`
FROM `CHAR_SET`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `font_name` ASC;
