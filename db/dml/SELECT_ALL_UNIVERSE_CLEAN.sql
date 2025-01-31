SELECT `univ_uid_pk`,
`univ_name`,
`radius_gly`,
`volume_gly3`,
`volume_pc3`,
`age_gyr`,
`expansion_rate_kmpsec_per_mpc`,
`total_mass_kg`,
`dark_energy_kg`,
`dark_matter_kg`,
`baryonic_matter_kg`,
`delete_dt`
FROM `UNIVERSE`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `univ_name` ASC;
