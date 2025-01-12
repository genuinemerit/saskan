SELECT `button_item_uid_pk`,
`button_multi_uid_fk`,
`button_id`,
`lang_code`,
`button_name`,
`button_icon`,
`button_icon_path`,
`button_order`,
`button_action`,
`enabled_by_default`,
`is_enabled`,
`help_text`,
`delete_dt`
FROM `BUTTON_ITEM`
WHERE delete_dt IS NULL OR delete_dt = ''
ORDER BY `button_name` ASC;
