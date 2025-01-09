CREATE TABLE IF NOT EXISTS LANG_FAMILY (
lang_family_uid_pk TEXT DEFAULT '',
char_set_uid_fk TEXT DEFAULT '',
lang_family_name TEXT DEFAULT '',
lang_family_desc TEXT DEFAULT '',
phonetics TEXT DEFAULT '',
cultural_influences TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
FOREIGN KEY (char_set_uid_fk) REFERENCES CHAR_SET(char_set_uid_pk) ON DELETE CASCADE,PRIMARY KEY (lang_family_uid_pk));
