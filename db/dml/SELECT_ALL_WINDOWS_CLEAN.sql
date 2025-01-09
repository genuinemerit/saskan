SELECT `win_uid_pk`,
`frame_uid_fk`,
`frame_id`,
`lang_code`,
`win_id`,
`win_title`,
`win_margin`,
`delete_dt`
FROM `WINDOWS`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `win_id` ASC, `lang_code` ASC;
