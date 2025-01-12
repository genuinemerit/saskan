UPDATE `WINDOWS` SET
`frame_uid_fk`=?,
`frame_id`=?,
`lang_code`=?,
`win_id`=?,
`win_name`=?,
`win_margin`=?,
`delete_dt`=?
WHERE `win_uid_pk`=?;
