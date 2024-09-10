SELECT river_uid_pk, gloss_common_uid_fk, river_course_points_json, river_bank_points_json, river_type, avg_width_m, avg_depth_m, total_length_km, drainage_basin_km, avg_velocity_m_per_h, gradient_m_per_km, river_hazards_json, river_features_json, river_nav_type, flora_and_fauna, water_quality, historical_events, current_conditions, delete_dt
FROM RIVER
WHERE river_uid_pk=?
ORDER BY river_uid_pk ASC;
