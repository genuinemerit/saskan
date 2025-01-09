UPDATE `BUTTON_SINGLE` SET
`button_type`=?,
`button_name`=?,
`button_icon`=?,
`button_icon_path`=?,
`button_key`=?,
`frame_uid_fk`=?,
`window_uid_fk`=?,
`left_x`=?,
`top_y`=?,
`enabled_by_default`=?,
`help_text`=?,
`action`=?,
`delete_dt`=?
WHERE `button_single_uid_pk`=?;
