SELECT `external_univ_uid_pk`, `univ_uid_fk`, `external_univ_name`, `mass_kg`, `dark_energy_kg`, `dark_matter_kg`, `baryonic_matter_kg`, `delete_dt`
FROM `EXTERNAL_UNIVERSE`
WHERE `external_univ_uid_pk` = ?
ORDER BY `external_univ_name ASC`;