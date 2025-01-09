SELECT `button_multi_uid_pk`,
`button_type`,
`button_name`,
`button_icon`,
`button_icon_path`,
`frame_uid_fk`,
`window_uid_fk`,
`left_x`,
`top_y`,
`enabled_by_default`,
`help_text`,
`delete_dt`
FROM `BUTTON_MULTI`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `button_name` ASC;
