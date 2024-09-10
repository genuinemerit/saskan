SELECT menu_bar_uid_pk, frame_uid_fk, frame_id, mbar_margin, mbar_h, mbar_x, mbar_y, delete_dt
FROM MENU_BARS
WHERE menu_bar_uid_pk=?
ORDER BY frame_id ASC;
