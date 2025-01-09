SELECT `menu_bar_uid_pk`,
`frame_uid_fk`,
`frame_id`,
`mbar_margin`,
`mbar_h`,
`mbar_x`,
`mbar_y`,
`delete_dt`
FROM `MENU_BARS`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `frame_id` ASC;
