CREATE TABLE IF NOT EXISTS MENU_ITEMS (
item_uid_pk TEXT DEFAULT '',
menu_uid_fk TEXT DEFAULT '',
lang_uid_fk TEXT DEFAULT '',
version_id TEXT DEFAULT '',
item_id TEXT DEFAULT '',
item_order INTEGER DEFAULT 0,
item_name TEXT DEFAULT '',
help_text TEXT DEFAULT '',
enabled_default BOOLEAN DEFAULT 1,
FOREIGN KEY (menu_uid_fk) REFERENCES MENUS(menu_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (lang_uid_fk) REFERENCES LANGUAGE(lang_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (item_uid_pk));
