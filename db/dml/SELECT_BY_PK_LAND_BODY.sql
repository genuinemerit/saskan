SELECT land_body_uid_pk, gloss_common_uid_fk, body_landline_points_json, land_body_type, land_body_surface_area_m2, land_body_surface_avg_altitude_m, max_altitude_m, min_altitude_m, delete_dt
FROM LAND_BODY
WHERE l=? AND a=? AND n=? AND d=? AND _=? AND b=? AND o=? AND d=? AND y=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY land_body_uid_pk ASC;
