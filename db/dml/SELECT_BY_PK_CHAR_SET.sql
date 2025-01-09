SELECT `char_set_uid_pk`, `font_name`, `char_set_type`, `char_set_desc`, `delete_dt`
FROM `CHAR_SET`
WHERE `char_set_uid_pk` = ?
ORDER BY `font_name ASC`;
