CREATE TABLE IF NOT EXISTS GALACTIC_CLUSTER (
galactic_cluster_uid_pk TEXT DEFAULT '',
univ_uid_fk TEXT DEFAULT '',
galactic_cluster_name TEXT DEFAULT '',
-- GROUP center_from_univ_center_gly: <class 'io_data.Struct.CoordXYZ'>
center_from_univ_center_gly_x NUMERIC DEFAULT 0.0,
center_from_univ_center_gly_y NUMERIC DEFAULT 0.0,
center_from_univ_center_gly_z NUMERIC DEFAULT 0.0,
-- GROUP boundary_gly: <class 'io_data.Struct.Game3DLocation'>
boundary_gly_origin_x NUMERIC DEFAULT 0.0,
boundary_gly_origin_y NUMERIC DEFAULT 0.0,
boundary_gly_origin_z NUMERIC DEFAULT 0.0,
boundary_gly_width_x NUMERIC DEFAULT 0.0,
boundary_gly_height_y NUMERIC DEFAULT 0.0,
boundary_gly_depth_z NUMERIC DEFAULT 0.0,
cluster_shape TEXT DEFAULT 'ellipsoid',
-- GROUP shape_pc: <class 'io_data.Struct.CoordXYZ'>
shape_pc_x NUMERIC DEFAULT 0.0,
shape_pc_y NUMERIC DEFAULT 0.0,
shape_pc_z NUMERIC DEFAULT 0.0,
-- GROUP shape_axes: <class 'io_data.Struct.AxesABC'>
shape_axes_a NUMERIC DEFAULT 0.0,
shape_axes_b NUMERIC DEFAULT 0.0,
shape_axes_c NUMERIC DEFAULT 0.0,
-- GROUP shape_rot: <class 'io_data.Struct.PitchYawRollAngle'>
shape_rot_pitch NUMERIC DEFAULT 0.0,
shape_rot_yaw NUMERIC DEFAULT 0.0,
shape_rot_roll NUMERIC DEFAULT 0.0,
volume_pc3 NUMERIC DEFAULT 0.0,
mass_kg NUMERIC DEFAULT 0.0,
dark_energy_kg NUMERIC DEFAULT 0.0,
dark_matter_kg NUMERIC DEFAULT 0.0,
baryonic_matter_kg NUMERIC DEFAULT 0.0,
timing_pulsar_pulse_per_ms NUMERIC DEFAULT 0.0,
-- GROUP timing_pulsar_loc_gly: <class 'io_data.Struct.CoordXYZ'>
timing_pulsar_loc_gly_x NUMERIC DEFAULT 0.0,
timing_pulsar_loc_gly_y NUMERIC DEFAULT 0.0,
timing_pulsar_loc_gly_z NUMERIC DEFAULT 0.0,
CHECK (cluster_shape IN ('ellipsoid', 'spherical')),
FOREIGN KEY (univ_uid_fk) REFERENCES UNIVERSE(univ_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (galactic_cluster_uid_pk));
