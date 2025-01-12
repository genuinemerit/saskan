SELECT `button_single_uid_pk`,
`frame_uid_fk`,
`window_uid_fk`,
`button_type`,
`button_id`,
`lang_code`,
`button_name`,
`button_icon`,
`button_icon_path`,
`button_key`,
`left_x`,
`top_y`,
`enabled_by_default`,
`help_text`,
`action`,
`delete_dt`
FROM `BUTTON_SINGLE`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `button_name` ASC;
