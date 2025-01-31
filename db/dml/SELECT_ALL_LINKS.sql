SELECT `link_uid_pk`,
`lang_code`,
`link_id`,
`frame_id`,
`link_protocol`,
`mime_type`,
`link_name`,
`link_uri`,
`link_icon`,
`link_icon_path`,
`delete_dt`
FROM `LINKS`
ORDER BY `frame_id` ASC, `link_id` ASC, `lang_code` ASC;
