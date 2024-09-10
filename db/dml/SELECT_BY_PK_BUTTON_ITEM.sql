SELECT button_item_uid_pk, button_multi_uid_fk, button_name, button_icon, button_order, button_action, is_enabled, help_text, delete_dt
FROM BUTTON_ITEM
WHERE button_item_uid_pk=?
ORDER BY button_name ASC;
