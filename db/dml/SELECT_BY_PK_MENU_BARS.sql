SELECT menu_bar_uid_pk, frame_uid_fk, version_id, menu_bar_name, link_value
FROM MENU_BARS
WHERE menu_bar_uid_pk=?
ORDER BY menu_bar_name ASC, version_id ASC;
