SELECT land_body_uid_pk, gloss_common_uid_fk, body_landline_points_json, land_body_type, land_body_surface_area_m2, land_body_surface_avg_altitude_m, max_altitude_m, min_altitude_m, delete_dt
FROM LAND_BODY
WHERE land_body_uid_pk=?
ORDER BY land_body_uid_pk ASC;
