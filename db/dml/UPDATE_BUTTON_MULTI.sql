UPDATE `BUTTON_MULTI` SET
`button_type`=?,
`button_name`=?,
`button_icon`=?,
`button_icon_path`=?,
`frame_uid_fk`=?,
`window_uid_fk`=?,
`left_x`=?,
`top_y`=?,
`enabled_by_default`=?,
`help_text`=?,
`delete_dt`=?
WHERE `button_multi_uid_pk`=?;