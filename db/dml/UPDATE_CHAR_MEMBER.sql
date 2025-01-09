UPDATE `CHAR_MEMBER` SET
`char_set_uid_fk`=?,
`char_member_name`=?,
`char_member_image`=?,
`char_member_path`=?,
`char_member_desc`=?,
`delete_dt`=?
WHERE `char_member_uid_pk`=?;
