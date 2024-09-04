SELECT bkup_uid_pk,
bkup_name,
bkup_dttm,
bkup_type,
file_from,
file_to
FROM BACKUP
ORDER BY bkup_dttm DESC, bkup_name ASC;
