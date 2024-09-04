CREATE TABLE IF NOT EXISTS UNIVERSE (
univ_uid_pk TEXT DEFAULT '',
univ_name TEXT DEFAULT '',
radius_gly NUMERIC DEFAULT 0.0,
volume_gly3 NUMERIC DEFAULT 0.0,
volume_pc3 NUMERIC DEFAULT 0.0,
age_gyr NUMERIC DEFAULT 0.0,
expansion_rate_kmpsec_per_mpc NUMERIC DEFAULT 0.0,
total_mass_kg NUMERIC DEFAULT 0.0,
dark_energy_kg NUMERIC DEFAULT 0.0,
dark_matter_kg NUMERIC DEFAULT 0.0,
baryonic_matter_kg NUMERIC DEFAULT 0.0,
PRIMARY KEY (univ_uid_pk));
