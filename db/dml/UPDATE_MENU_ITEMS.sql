UPDATE MENU_ITEMS SET
menu_uid_fk=?,
lang_code=?,
frame_id=?,
item_id=?,
item_order=?,
item_name=?,
key_binding=?,
help_text=?,
enabled_default=?,
delete_dt=?
WHERE item_uid_pk=?;
