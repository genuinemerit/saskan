SELECT `char_member_uid_pk`,
`char_set_uid_fk`,
`char_member_name`,
`char_member_image`,
`char_member_path`,
`char_member_desc`,
`delete_dt`
FROM `CHAR_MEMBER`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `char_member_name` ASC;
