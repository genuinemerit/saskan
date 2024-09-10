SELECT lunar_year_x_moon_uid_pk, lunar_year_uid_fk, moon_uid_fk, delete_dt
FROM LUNAR_YEAR_X_MOON
WHERE lunar_year_x_moon_uid_pk=?;
