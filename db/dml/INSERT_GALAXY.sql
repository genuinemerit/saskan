INSERT INTO GALAXY (
galaxy_uid_pk,
galactic_cluster_uid_fk,
galaxy_name,
relative_size,
center_from_univ_center_kpc_x,
center_from_univ_center_kpc_y,
center_from_univ_center_kpc_z,
halo_radius_pc,
boundary_pc_origin_x,
boundary_pc_origin_y,
boundary_pc_origin_z,
boundary_pc_width_x,
boundary_pc_height_y,
boundary_pc_depth_z,
volume_gpc3,
mass_kg,
bulge_shape,
bulge_center_from_center_ly_x,
bulge_center_from_center_ly_y,
bulge_center_from_center_ly_z,
bulge_dim_axes_a,
bulge_dim_axes_b,
bulge_dim_axes_c,
bulge_dim_rot_pitch,
bulge_dim_rot_yaw,
bulge_dim_rot_roll,
bulge_black_hole_mass_kg,
bulge_volume_ly3,
bulge_total_mass_kg,
star_field_shape,
star_field_dim_from_center_ly_x,
star_field_dim_from_center_ly_y,
star_field_dim_from_center_ly_z,
star_field_dim_axes_a,
star_field_dim_axes_b,
star_field_dim_axes_c,
star_field_dim_rot_pitch,
star_field_dim_rot_yaw,
star_field_dim_rot_roll,
star_field_vol_ly3,
star_field_mass_kg,
interstellar_mass_kg,
delete_dt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
