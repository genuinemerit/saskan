UPDATE MOON SET
world_uid_fk=?,
moon_name=?,
mass_kg=?,
radius_km=?,
obliquity_dg=?,
is_tidally_locked=?,
rotation_direction=?,
orbit_direction=?,
orbit_world_days=?,
rotation_world_days=?,
initial_velocity=?,
angular_velocity=?
WHERE moon_uid_pk=?;
