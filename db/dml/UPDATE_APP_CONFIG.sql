UPDATE APP_CONFIG SET
version_id=?,
root_dir=?,
mem_dir=?,
cfg_dir=?,
dat_dir=?,
html_dir=?,
img_dir=?,
snd_dir=?,
py_dir=?,
db_dir=?,
log_dir=?,
mon_dir=?,
dbg_dir=?
WHERE config_uid_pk=?;
