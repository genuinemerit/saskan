SELECT item_uid_pk, menu_uid_fk, lang_uid_fk, version_id, item_id, item_order, item_name, help_text, enabled_default
FROM MENU_ITEMS
WHERE item_uid_pk=?
ORDER BY item_id ASC, item_name ASC;
