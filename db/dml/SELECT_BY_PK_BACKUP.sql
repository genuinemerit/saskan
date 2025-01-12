SELECT `bkup_uid_pk`, `bkup_id`, `bkup_dttm`, `bkup_type`, `file_from`, `file_to`, `delete_dt`
FROM `BACKUP`
WHERE `bkup_uid_pk` = ?
ORDER BY `bkup_dttm DESC`, `bkup_id ASC`;
