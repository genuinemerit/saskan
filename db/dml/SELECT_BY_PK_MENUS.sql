SELECT menu_uid_pk, menu_bar_uid_fk, frame_id, lang_code, version_id, menu_id, menu_name
FROM MENUS
WHERE menu_uid_pk=?
ORDER BY menu_id ASC, lang_code ASC, menu_name ASC;
