SELECT `button_single_uid_pk`, `button_type`, `button_name`, `button_icon`, `button_icon_path`, `button_key`, `frame_uid_fk`, `window_uid_fk`, `left_x`, `top_y`, `enabled_by_default`, `help_text`, `action`, `delete_dt`
FROM `BUTTON_SINGLE`
WHERE `button_single_uid_pk` = ?
ORDER BY `button_name ASC`;
