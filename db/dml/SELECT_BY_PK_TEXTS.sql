SELECT text_uid_pk, lang_code, text_name, text_value, delete_dt
FROM TEXTS
WHERE t=? AND e=? AND x=? AND t=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY text_name ASC, lang_code ASC;
