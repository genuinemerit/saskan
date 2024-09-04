UPDATE MENU_ITEMS SET
menu_uid_fk=?,
lang_uid_fk=?,
version_id=?,
item_id=?,
item_order=?,
item_name=?,
help_text=?,
enabled_default=?
WHERE item_uid_pk=?;
