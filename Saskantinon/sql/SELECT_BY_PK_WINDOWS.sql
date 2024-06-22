SELECT win_uid_pk, frame_uid_fk, lang_uid_fk, version_id, win_name, win_title, win_x, win_y, win_w, win_h, win_margin
FROM WINDOWS
WHERE win_uid_pk=?
ORDER BY win_name ASC, version_id ASC;
