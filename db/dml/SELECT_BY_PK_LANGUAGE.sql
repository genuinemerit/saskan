SELECT lang_uid_pk, lang_family_uid_fk, lang_name, lang_desc, gramatics, lexicals, social_influences, word_formations, delete_dt
FROM LANGUAGE
WHERE l=? AND a=? AND n=? AND g=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY lang_name ASC;
