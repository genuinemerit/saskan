SELECT gloss_common_uid_pk, dialect_uid_fk, gloss_type, gloss_name, gloss_value, gloss_uri, delete_dt
FROM GLOSS_COMMON
WHERE g=? AND l=? AND o=? AND s=? AND s=? AND _=? AND c=? AND o=? AND m=? AND m=? AND o=? AND n=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY gloss_name ASC;
