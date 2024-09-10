SELECT lang_family_uid_pk, char_set_uid_fk, lang_family_name, lang_family_desc, phonetics, cultural_influences, delete_dt
FROM LANG_FAMILY
WHERE lang_family_uid_pk=?
ORDER BY lang_family_name ASC;
