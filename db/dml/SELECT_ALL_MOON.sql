SELECT `moon_uid_pk`,
`world_uid_fk`,
`moon_name`,
`moon_desc`,
`moon_lore`,
`center_from_world_center_km`,
`mass_kg`,
`radius_km`,
`obliquity_dg`,
`is_tidally_locked`,
`rotation_direction`,
`orbit_direction`,
`orbit_world_days`,
`rotation_world_days`,
`initial_velocity`,
`angular_velocity`,
`delete_dt`
FROM `MOON`
ORDER BY `moon_name` ASC;
