SELECT button_single_uid_pk, button_type, button_name, button_icon, button_key, frame_uid_fk, window_uid_fk, x, y, enabled, help_text, action, delete_dt
FROM BUTTON_SINGLE
WHERE b=? AND u=? AND t=? AND t=? AND o=? AND n=? AND _=? AND s=? AND i=? AND n=? AND g=? AND l=? AND e=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY button_name ASC;
