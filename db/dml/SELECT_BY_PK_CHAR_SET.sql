SELECT char_set_uid_pk, char_set_name, char_set_type, char_set_desc, delete_dt
FROM CHAR_SET
WHERE c=? AND h=? AND a=? AND r=? AND _=? AND s=? AND e=? AND t=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY char_set_name ASC;
