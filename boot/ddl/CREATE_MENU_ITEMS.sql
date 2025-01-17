CREATE TABLE IF NOT EXISTS MENU_ITEMS (
item_uid_pk TEXT DEFAULT '',
menu_uid_fk TEXT DEFAULT '',
lang_code TEXT DEFAULT '',
frame_id TEXT DEFAULT '',
item_id TEXT DEFAULT '',
item_order INTEGER DEFAULT 0,
item_name TEXT DEFAULT '',
key_binding TEXT DEFAULT '',
help_text TEXT DEFAULT '',
enabled_by_default BOOLEAN DEFAULT 1,
delete_dt TEXT DEFAULT '',
CHECK (lang_code IN ('en')),
FOREIGN KEY (menu_uid_fk) REFERENCES MENUS(menu_uid_pk) ON DELETE CASCADE,PRIMARY KEY (item_uid_pk));
