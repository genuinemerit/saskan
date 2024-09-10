SELECT galactic_cluster_uid_pk, univ_uid_fk, galactic_cluster_name, center_from_univ_center_gly_x, center_from_univ_center_gly_y, center_from_univ_center_gly_z, boundary_gly_origin_x, boundary_gly_origin_y, boundary_gly_origin_z, boundary_gly_width_x, boundary_gly_height_y, boundary_gly_depth_z, cluster_shape, shape_pc_x, shape_pc_y, shape_pc_z, shape_axes_a, shape_axes_b, shape_axes_c, shape_rot_pitch, shape_rot_yaw, shape_rot_roll, volume_pc3, mass_kg, dark_energy_kg, dark_matter_kg, baryonic_matter_kg, timing_pulsar_pulse_per_ms, timing_pulsar_loc_gly_x, timing_pulsar_loc_gly_y, timing_pulsar_loc_gly_z, delete_dt
FROM GALACTIC_CLUSTER
WHERE galactic_cluster_uid_pk=?
ORDER BY galactic_cluster_name ASC;
