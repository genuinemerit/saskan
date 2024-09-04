SELECT text_uid_pk, lang_code, text_name, text_value
FROM TEXTS
WHERE text_uid_pk=?
ORDER BY text_name ASC, lang_code ASC;
