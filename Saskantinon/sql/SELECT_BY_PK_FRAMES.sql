SELECT frame_uid_pk, lang_uid_fk, app_catg, version_id, frame_name, frame_title, frame_desc, size_w, size_h, ibar_x, ibar_y, pg_hdr_x, pg_hdr_y, pg_hdr_w, pg_hdr_h, pg_hdr_txt
FROM FRAMES
WHERE frame_uid_pk=?
ORDER BY app_catg ASC, frame_name ASC, version_id ASC;
