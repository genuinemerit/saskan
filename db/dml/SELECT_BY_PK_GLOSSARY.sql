SELECT glossary_uid_pk, gloss_common_uid_fk, dialect_uid_fk, gloss_type, gloss_name, gloss_value, gloss_uri
FROM GLOSSARY
WHERE glossary_uid_pk=?
ORDER BY gloss_name ASC;
