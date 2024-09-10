SELECT ocean_body_uid_pk, gloss_common_uid_fk, body_shoreline_points_json, is_coastal, is_frozen, ocean_body_type, water_type, is_tidal_influence, tidal_flows_per_day, avg_high_tide_m, avg_low_tide_m, max_high_tide_m, ocean_wave_type, body_surface_area_m2, body_surface_altitude_m, max_depth_m, avg_depth_m, ocean_hazards_json, ocean_features_json, delete_dt
FROM OCEAN_BODY
WHERE ocean_body_uid_pk=?
ORDER BY ocean_body_uid_pk ASC;
