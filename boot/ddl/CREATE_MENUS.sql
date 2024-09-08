CREATE TABLE IF NOT EXISTS MENUS (
menu_uid_pk TEXT DEFAULT '',
menu_bar_uid_fk TEXT DEFAULT '',
lang_uid_fk TEXT DEFAULT '',
version_id TEXT DEFAULT '',
menu_id TEXT DEFAULT '',
menu_name TEXT DEFAULT '',
FOREIGN KEY (menu_bar_uid_fk) REFERENCES MENU_BARS(menu_bar_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (lang_uid_fk) REFERENCES LANGUAGE(lang_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (menu_uid_pk));
