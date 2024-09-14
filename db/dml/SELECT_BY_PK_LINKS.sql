SELECT link_uid_pk, lang_code, link_id, frame_id, link_protocol, mime_type, link_name, link_value, link_icon, delete_dt
FROM LINKS
WHERE l=? AND i=? AND n=? AND k=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY frame_id ASC, link_id ASC, lang_code ASC;
