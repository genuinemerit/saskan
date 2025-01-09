CREATE TABLE IF NOT EXISTS LUNAR_YEAR (
lunar_year_uid_pk TEXT DEFAULT '',
world_uid_fk TEXT DEFAULT '',
lang_uid_vfk TEXT DEFAULT '',
lunar_year_name TEXT DEFAULT '',
lunar_year_desc TEXT DEFAULT '',
days_in_lunar_year NUMERIC DEFAULT 0.0,
delete_dt TEXT DEFAULT '',
FOREIGN KEY (world_uid_fk) REFERENCES WORLD(world_uid_pk) ON DELETE CASCADE,PRIMARY KEY (lunar_year_uid_pk));
