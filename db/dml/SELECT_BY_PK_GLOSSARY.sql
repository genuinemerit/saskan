SELECT glossary_uid_pk, gloss_common_uid_fk, dialect_uid_fk, gloss_type, gloss_name, gloss_value, gloss_uri, delete_dt
FROM GLOSSARY
WHERE g=? AND l=? AND o=? AND s=? AND s=? AND a=? AND r=? AND y=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY gloss_name ASC;
