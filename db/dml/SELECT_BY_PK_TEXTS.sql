SELECT `text_uid_pk`, `lang_code`, `text_id`, `text_value`, `delete_dt`
FROM `TEXTS`
WHERE `text_uid_pk` = ?
ORDER BY `text_id ASC`, `lang_code ASC`;
