INSERT INTO MENU_ITEMS (
item_uid_pk,
menu_uid_fk,
lang_code,
frame_id,
item_id,
item_order,
item_name,
key_binding,
help_text,
enabled_default,
delete_dt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
