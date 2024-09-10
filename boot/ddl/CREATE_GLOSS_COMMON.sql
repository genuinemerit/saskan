CREATE TABLE IF NOT EXISTS GLOSS_COMMON (
gloss_common_uid_pk TEXT DEFAULT '',
dialect_uid_fk TEXT DEFAULT '',
gloss_type TEXT DEFAULT '',
gloss_name TEXT DEFAULT '',
gloss_value TEXT DEFAULT '',
gloss_uri TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (gloss_type IN ('word', 'phrase', 'map', 'picture', 'diagram', 'data', 'software', 'sound', 'video')),
FOREIGN KEY (dialect_uid_fk) REFERENCES LANG_DIALECT(dialect_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (gloss_common_uid_pk));
