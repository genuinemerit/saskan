SELECT menu_bar_uid_pk,
frame_uid_fk,
lang_code,
version_id,
frame_id,
mbar_margin,
mbar_h,
mbar_x,
mbar_y
FROM MENU_BARS
ORDER BY frame_id ASC, version_id ASC;
