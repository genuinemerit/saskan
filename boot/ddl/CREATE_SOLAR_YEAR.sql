CREATE TABLE IF NOT EXISTS SOLAR_YEAR (
solar_year_uid_pk TEXT DEFAULT '',
world_uid_fk TEXT DEFAULT '',
lang_uid_fk TEXT DEFAULT '',
solar_year_key TEXT DEFAULT '',
version_id TEXT DEFAULT '',
solar_year_name TEXT DEFAULT '',
solar_year_desc TEXT DEFAULT '',
solar_year_span NUMERIC DEFAULT 0.0,
days_in_solar_year NUMERIC DEFAULT 0.0,
delete_dt TEXT DEFAULT '',
FOREIGN KEY (world_uid_fk) REFERENCES WORLD(world_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (lang_uid_fk) REFERENCES LANGUAGE(lang_uid_pk) ON DELETE CASCADE,PRIMARY KEY (solar_year_uid_pk));
