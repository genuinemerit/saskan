CREATE TABLE IF NOT EXISTS MENUS (
menu_uid_pk TEXT DEFAULT '',
menu_bar_uid_fk TEXT DEFAULT '',
frame_id TEXT DEFAULT '',
lang_code TEXT DEFAULT '',
menu_id TEXT DEFAULT '',
menu_name TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (lang_code IN ('en')),
FOREIGN KEY (menu_bar_uid_fk) REFERENCES MENU_BARS(menu_bar_uid_pk) ON DELETE CASCADE,PRIMARY KEY (menu_uid_pk));
