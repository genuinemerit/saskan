CREATE TABLE IF NOT EXISTS SEASON (
season_uid_pk TEXT DEFAULT '',
solar_year_uid_fk TEXT DEFAULT '',
gloss_common_uid_fk TEXT DEFAULT '',
version_id TEXT DEFAULT '',
season_type TEXT DEFAULT '',
hemisphere_type TEXT DEFAULT '',
years_in_season NUMERIC DEFAULT 0.0,
delete_dt TEXT DEFAULT '',
CHECK (season_type IN ('winter', 'spring', 'summer', 'fallall', 'winter-spring', 'spring-summer', 'summer-fall', 'fall-winter')),
CHECK (hemisphere_type IN ('north', 'south')),
FOREIGN KEY (solar_year_uid_fk) REFERENCES SOLAR_YEAR(solar_year_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (gloss_common_uid_fk) REFERENCES GLOSS_COMMON(gloss_common_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (season_uid_pk));
