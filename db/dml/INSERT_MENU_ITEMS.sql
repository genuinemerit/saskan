INSERT INTO MENU_ITEMS (
item_uid_pk,
menu_uid_fk,
lang_uid_fk,
version_id,
item_id,
item_order,
item_name,
help_text,
enabled_default) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
