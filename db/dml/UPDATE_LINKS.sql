UPDATE `LINKS` SET
`lang_code`=?,
`link_id`=?,
`frame_id`=?,
`link_protocol`=?,
`mime_type`=?,
`link_name`=?,
`link_value`=?,
`link_icon`=?,
`link_icon_path`=?,
`delete_dt`=?
WHERE `link_uid_pk`=?;
