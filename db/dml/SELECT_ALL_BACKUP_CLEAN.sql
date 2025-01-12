SELECT `bkup_uid_pk`,
`bkup_id`,
`bkup_dttm`,
`bkup_type`,
`file_from`,
`file_to`,
`delete_dt`
FROM `BACKUP`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `bkup_dttm` DESC, `bkup_id` ASC;
