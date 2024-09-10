SELECT button_single_uid_pk,
button_type,
button_name,
button_icon,
button_key,
frame_uid_fk,
window_uid_fk,
x,
y,
enabled,
help_text,
action,
delete_dt
FROM BUTTON_SINGLE
ORDER BY button_name ASC;
