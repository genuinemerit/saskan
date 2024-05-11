SELECT gloss_common_uid_pk,
dialect_uid_fk,
gloss_type,
gloss_name,
gloss_value,
gloss_uri
FROM GLOSS_COMMON
ORDER BY gloss_name ASC;
