SELECT win_uid_pk,
frame_uid_fk,
frame_id,
lang_code,
version_id,
win_id,
win_title,
win_margin
FROM WINDOWS
ORDER BY win_id ASC, lang_code ASC, version_id ASC;
