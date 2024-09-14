SELECT star_system_uid_pk, galaxy_uid_fk, star_system_name, is_black_hole, is_pulsar, boundary_pc_origin_x, boundary_pc_origin_y, boundary_pc_origin_z, boundary_pc_width_x, boundary_pc_height_y, boundary_pc_depth_z, volume_pc3, mass_kg, system_shape, center_from_galaxy_center_pc_x, center_from_galaxy_center_pc_y, center_from_galaxy_center_pc_z, system_dim_axes_a, system_dim_axes_b, system_dim_axes_c, system_dim_rot_pitch, system_dim_rot_yaw, system_dim_rot_roll, relative_size, spectral_class, aprox_age_gyr, luminosity_class, frequency_of_flares, intensity_of_flares, frequency_of_comets, unbound_planets_cnt, orbiting_planets_cnt, inner_habitable_boundary_au, outer_habitable_boundary_au, planetary_orbits_shape, orbital_stability, asteroid_belt_density, asteroid_belt_loc, delete_dt
FROM STAR_SYSTEM
WHERE s=? AND t=? AND a=? AND r=? AND _=? AND s=? AND y=? AND s=? AND t=? AND e=? AND m=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY star_system_name ASC;
