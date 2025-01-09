UPDATE `EXTERNAL_UNIVERSE` SET
`univ_uid_fk`=?,
`external_univ_name`=?,
`mass_kg`=?,
`dark_energy_kg`=?,
`dark_matter_kg`=?,
`baryonic_matter_kg`=?,
`delete_dt`=?
WHERE `external_univ_uid_pk`=?;
