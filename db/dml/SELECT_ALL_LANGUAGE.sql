SELECT lang_uid_pk,
lang_family_uid_fk,
lang_name,
lang_desc,
gramatics,
lexicals,
social_influences,
word_formations,
delete_dt
FROM LANGUAGE
ORDER BY lang_name ASC;
