SELECT bkup_uid_pk, bkup_name, bkup_dttm, bkup_type, file_from, file_to, delete_dt
FROM BACKUP
WHERE b=? AND k=? AND u=? AND p=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY bkup_dttm DESC, bkup_name ASC;
