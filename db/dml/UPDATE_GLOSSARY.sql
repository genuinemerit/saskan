UPDATE GLOSSARY SET
gloss_common_uid_fk=?,
dialect_uid_fk=?,
gloss_type=?,
gloss_name=?,
gloss_value=?,
gloss_uri=?
WHERE glossary_uid_pk=?;
