SELECT char_set_uid_pk, char_set_name, char_set_type, char_set_desc
FROM CHAR_SET
WHERE char_set_uid_pk=?
ORDER BY char_set_name ASC;
