SELECT link_uid_pk,
version_id,
lang_uid_fk,
link_catg,
link_name,
link_value
FROM LINKS
ORDER BY link_catg ASC, link_name ASC, version_id ASC;