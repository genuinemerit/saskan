SELECT `button_multi_uid_pk`,
`frame_uid_fk`,
`window_uid_fk`,
`button_type`,
`button_id`,
`lang_code`,
`button_name`,
`button_icon`,
`button_icon_path`,
`left_x`,
`top_y`,
`enabled_by_default`,
`help_text`,
`delete_dt`
FROM `BUTTON_MULTI`
ORDER BY `button_name` ASC;
