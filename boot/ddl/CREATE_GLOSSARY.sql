CREATE TABLE IF NOT EXISTS GLOSSARY (
glossary_uid_pk TEXT DEFAULT '',
gloss_common_uid_fk TEXT DEFAULT '',
dialect_uid_fk TEXT DEFAULT '',
gloss_type TEXT DEFAULT '',
gloss_name TEXT DEFAULT '',
gloss_value TEXT DEFAULT '',
gloss_uri TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (gloss_type IN ('word', 'phrase', 'map', 'picture', 'diagram', 'data', 'software', 'sound', 'video')),
FOREIGN KEY (gloss_common_uid_fk) REFERENCES GLOSS_COMMON(gloss_common_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (dialect_uid_fk) REFERENCES LANG_DIALECT(dialect_uid_pk) ON DELETE CASCADE,PRIMARY KEY (glossary_uid_pk));
