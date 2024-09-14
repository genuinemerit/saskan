SELECT moon_uid_pk, world_uid_fk, moon_name, mass_kg, radius_km, obliquity_dg, is_tidally_locked, rotation_direction, orbit_direction, orbit_world_days, rotation_world_days, initial_velocity, angular_velocity, delete_dt
FROM MOON
WHERE m=? AND o=? AND o=? AND n=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY moon_name ASC;
