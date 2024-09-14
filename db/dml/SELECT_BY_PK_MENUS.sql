SELECT menu_uid_pk, menu_bar_uid_fk, frame_id, lang_code, menu_id, menu_name, delete_dt
FROM MENUS
WHERE m=? AND e=? AND n=? AND u=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY menu_id ASC, lang_code ASC, menu_name ASC;
