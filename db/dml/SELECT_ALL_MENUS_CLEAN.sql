SELECT `menu_uid_pk`,
`menu_bar_uid_fk`,
`frame_id`,
`lang_code`,
`menu_id`,
`menu_name`,
`delete_dt`
FROM `MENUS`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `menu_id` ASC, `lang_code` ASC, `menu_name` ASC;
