CREATE TABLE IF NOT EXISTS LANGUAGE (
lang_uid_pk TEXT DEFAULT '',
lang_family_uid_fk TEXT DEFAULT '',
lang_name TEXT DEFAULT '',
lang_desc TEXT DEFAULT '',
gramatics TEXT DEFAULT '',
lexicals TEXT DEFAULT '',
social_influences TEXT DEFAULT '',
word_formations TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
FOREIGN KEY (lang_family_uid_fk) REFERENCES LANG_FAMILY(lang_family_uid_pk) ON DELETE CASCADE,PRIMARY KEY (lang_uid_pk));
