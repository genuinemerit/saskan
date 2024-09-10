SELECT item_uid_pk,
menu_uid_fk,
lang_code,
frame_id,
item_id,
item_order,
item_name,
key_binding,
help_text,
enabled_default,
delete_dt
FROM MENU_ITEMS
ORDER BY item_id ASC, lang_code ASC, item_name ASC;
