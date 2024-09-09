SELECT button_item_uid_pk, version_id, button_multi_uid_pk, button_name, button_icon, order, enabled, help_text, action
FROM BUTTON_ITEM
WHERE button_item_uid_pk=?
ORDER BY button_name ASC;
