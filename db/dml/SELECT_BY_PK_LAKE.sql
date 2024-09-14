SELECT lake_uid_pk, gloss_common_uid_fk, lake_shoreline_points_json, lake_size, water_type, lake_type, is_tidal_influence, lake_surface_m2, max_depth_m, avg_depth_m, lake_altitude_m, catchment_area_radius_m, lake_origin, flora_and_fauna, water_color, accessibility, special_features, lake_usage, legends_or_myths, lake_history, conservation_status, current_conditions, delete_dt
FROM LAKE
WHERE l=? AND a=? AND k=? AND e=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY lake_uid_pk ASC;
