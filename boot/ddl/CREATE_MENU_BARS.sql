CREATE TABLE IF NOT EXISTS MENU_BARS (
menu_bar_uid_pk TEXT DEFAULT '',
frame_uid_fk TEXT DEFAULT '',
frame_id TEXT DEFAULT '',
mbar_margin NUMERIC DEFAULT 0.0,
mbar_h NUMERIC DEFAULT 0.0,
mbar_x NUMERIC DEFAULT 0.0,
mbar_y NUMERIC DEFAULT 0.0,
delete_dt TEXT DEFAULT '',
FOREIGN KEY (frame_uid_fk) REFERENCES FRAMES(frame_uid_pk) ON DELETE CASCADE,PRIMARY KEY (menu_bar_uid_pk));
