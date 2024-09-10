UPDATE BUTTON_MULTI SET
button_type=?,
button_name=?,
button_icon=?,
frame_uid_fk=?,
window_uid_fk=?,
x=?,
y=?,
enabled=?,
help_text=?,
delete_dt=?
WHERE button_multi_uid_pk=?;
