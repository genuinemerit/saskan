CREATE TABLE IF NOT EXISTS LUNAR_YEAR (
lunar_year_uid_pk TEXT DEFAULT '',
world_uid_fk TEXT DEFAULT '',
lang_uid_fk TEXT DEFAULT '',
lunar_year_key TEXT DEFAULT '',
version_id TEXT DEFAULT '',
lunar_year_name TEXT DEFAULT '',
lunar_year_desc TEXT DEFAULT '',
days_in_lunar_year NUMERIC DEFAULT 0.0,
FOREIGN KEY (world_uid_fk) REFERENCES WORLD(world_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (lang_uid_fk) REFERENCES LANGUAGE(lang_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (lunar_year_uid_pk));
