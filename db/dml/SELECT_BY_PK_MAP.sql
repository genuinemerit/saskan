SELECT map_uid_pk, version_id, map_name, map_type, unit_of_measure, origin_2d_lat, origin_2d_lon, width_e_w_2d, height_n_s_2d, avg_alt_m, min_alt_m, max_alt_m, origin_3d_x, origin_3d_y, origin_3d_z, width_3d, height_3d, depth_3d, delete_dt
FROM MAP
WHERE map_uid_pk=?
ORDER BY map_name ASC;
