SELECT link_uid_pk,
version_id,
lang_code,
link_id,
frame_id,
link_protocol,
mime_type,
link_name,
link_value,
link_icon
FROM LINKS
ORDER BY frame_id ASC, link_id ASC, lang_code ASC;
