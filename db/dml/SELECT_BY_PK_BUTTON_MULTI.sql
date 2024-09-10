SELECT button_multi_uid_pk, button_type, button_name, button_icon, frame_uid_fk, window_uid_fk, x, y, enabled, help_text, delete_dt
FROM BUTTON_MULTI
WHERE button_multi_uid_pk=?
ORDER BY button_name ASC;
