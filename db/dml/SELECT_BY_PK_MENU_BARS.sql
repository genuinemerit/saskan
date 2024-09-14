SELECT menu_bar_uid_pk, frame_uid_fk, frame_id, mbar_margin, mbar_h, mbar_x, mbar_y, delete_dt
FROM MENU_BARS
WHERE m=? AND e=? AND n=? AND u=? AND _=? AND b=? AND a=? AND r=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY frame_id ASC;
