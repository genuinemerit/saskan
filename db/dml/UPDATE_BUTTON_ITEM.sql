UPDATE `BUTTON_ITEM` SET
`button_multi_uid_fk`=?,
`button_id`=?,
`lang_code`=?,
`button_name`=?,
`button_icon`=?,
`button_icon_path`=?,
`button_order`=?,
`button_action`=?,
`enabled_by_default`=?,
`is_enabled`=?,
`help_text`=?,
`delete_dt`=?
WHERE `button_item_uid_pk`=?;
