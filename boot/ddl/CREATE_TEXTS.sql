CREATE TABLE IF NOT EXISTS TEXTS (
text_uid_pk TEXT DEFAULT '',
lang_code TEXT DEFAULT '',
text_name TEXT DEFAULT '',
text_value TEXT DEFAULT '',
CHECK (lang_code IN ('en')),
PRIMARY KEY (text_uid_pk));
