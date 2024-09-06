CREATE TABLE IF NOT EXISTS LUNAR_YEAR_X_MOON (
lunar_year_x_moon_uid_pk TEXT DEFAULT '',
lunar_year_uid_fk TEXT DEFAULT '',
moon_uid_fk TEXT DEFAULT '',
FOREIGN KEY (lunar_year_uid_fk) REFERENCES LUNAR_YEAR(lunar_year_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (moon_uid_fk) REFERENCES MOON(moon_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (lunar_year_x_moon_uid_pk));
