INSERT INTO MENU_ITEMS (
item_uid_pk,
menu_uid_fk,
lang_code,
frame_id,
version_id,
item_id,
item_order,
item_name,
key_binding,
help_text,
enabled_default) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
