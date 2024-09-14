SELECT win_uid_pk, frame_uid_fk, frame_id, lang_code, win_id, win_title, win_margin, delete_dt
FROM WINDOWS
WHERE w=? AND i=? AND n=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY win_id ASC, lang_code ASC;
