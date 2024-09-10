UPDATE BACKUP SET
bkup_name=?,
bkup_dttm=?,
bkup_type=?,
file_from=?,
file_to=?,
delete_dt=?
WHERE bkup_uid_pk=?;
