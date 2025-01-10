SELECT `world_uid_pk`, `star_system_uid_fk`, `world_name`, `world_type`, `obliquity_dg`, `distance_from_star_au`, `distance_from_star_km`, `radius_km`, `mass_kg`, `gravity_m_per_s_per_s`, `orbit_gdy`, `orbit_gyr`, `is_tidally_locked`, `rotation_gdy`, `rotation_direction`, `orbit_direction`, `moons_cnt`, `world_desc`, `atmosphere`, `sky_color`, `biosphere`, `sentients`, `climate`, `tech_level`, `terrain`, `delete_dt`
FROM `WORLD`
WHERE `world_uid_pk` = ?
ORDER BY `world_name ASC`;