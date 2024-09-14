SELECT char_member_uid_pk, char_set_uid_fk, char_member_name, char_member_uri, char_member_desc, delete_dt
FROM CHAR_MEMBER
WHERE c=? AND h=? AND a=? AND r=? AND _=? AND m=? AND e=? AND m=? AND b=? AND e=? AND r=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY char_member_name ASC;
