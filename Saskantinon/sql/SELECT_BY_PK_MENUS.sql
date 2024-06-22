SELECT menu_uid_pk, menu_bar_uid_fk, lang_uid_fk, version_id, menu_id, menu_name
FROM MENUS
WHERE menu_uid_pk=?
ORDER BY menu_id ASC, menu_name ASC;
