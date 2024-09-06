CREATE TABLE IF NOT EXISTS MENU_BARS (
menu_bar_uid_pk TEXT DEFAULT '',
frame_uid_fk TEXT DEFAULT '',
version_id TEXT DEFAULT '',
menu_bar_name TEXT DEFAULT '',
link_value TEXT DEFAULT '',
FOREIGN KEY (frame_uid_fk) REFERENCES FRAMES(frame_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (menu_bar_uid_pk));
