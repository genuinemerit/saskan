UPDATE `MENU_BARS` SET
`frame_uid_fk`=?,
`frame_id`=?,
`mbar_margin`=?,
`mbar_h`=?,
`mbar_x`=?,
`mbar_y`=?,
`delete_dt`=?
WHERE `menu_bar_uid_pk`=?;
