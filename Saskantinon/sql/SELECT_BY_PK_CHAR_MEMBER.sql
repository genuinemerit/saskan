SELECT char_member_uid_pk, char_set_uid_fk, char_member_name, char_member_uri, char_member_desc
FROM CHAR_MEMBER
WHERE char_member_uid_pk=?
ORDER BY char_member_name ASC;
