CREATE TABLE IF NOT EXISTS EXTERNAL_UNIVERSE (
external_univ_uid_pk TEXT DEFAULT '',
univ_uid_fk TEXT DEFAULT '',
external_univ_name TEXT DEFAULT '',
mass_kg NUMERIC DEFAULT 0.0,
dark_energy_kg NUMERIC DEFAULT 0.0,
dark_matter_kg NUMERIC DEFAULT 0.0,
baryonic_matter_kg NUMERIC DEFAULT 0.0,
delete_dt TEXT DEFAULT '',
FOREIGN KEY (univ_uid_fk) REFERENCES UNIVERSE(univ_uid_pk) ON DELETE CASCADE,PRIMARY KEY (external_univ_uid_pk));
