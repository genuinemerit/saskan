SELECT `text_uid_pk`,
`lang_code`,
`text_name`,
`text_value`,
`delete_dt`
FROM `TEXTS`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `text_name` ASC, `lang_code` ASC;
