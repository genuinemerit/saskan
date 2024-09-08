CREATE TABLE IF NOT EXISTS LINKS (
link_uid_pk TEXT DEFAULT '',
version_id TEXT DEFAULT '',
lang_uid_fk TEXT DEFAULT '',
link_catg TEXT DEFAULT '',
link_name TEXT DEFAULT '',
link_value TEXT DEFAULT '',
CHECK (link_catg IN ('help')),
FOREIGN KEY (lang_uid_fk) REFERENCES LANGUAGE(lang_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (link_uid_pk));
