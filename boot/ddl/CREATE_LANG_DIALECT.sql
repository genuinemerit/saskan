CREATE TABLE IF NOT EXISTS LANG_DIALECT (
dialect_uid_pk TEXT DEFAULT '',
lang_uid_fk TEXT DEFAULT '',
dialect_name TEXT DEFAULT '',
dialect_desc TEXT DEFAULT '',
divergence_factors TEXT DEFAULT '',
syncretic_factors TEXT DEFAULT '',
preservation_factors TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
FOREIGN KEY (lang_uid_fk) REFERENCES LANGUAGE(lang_uid_pk) ON DELETE CASCADE,PRIMARY KEY (dialect_uid_pk));
