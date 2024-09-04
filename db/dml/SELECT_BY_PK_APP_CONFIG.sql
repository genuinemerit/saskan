SELECT config_uid_pk, version_id, root_dir, bin_dir, mem_dir, cfg_dir, dat_dir, img_dir, py_dir, db_dir, sch_dir, log_dat, mon_dat, dbg_dat
FROM APP_CONFIG
WHERE config_uid_pk=?
ORDER BY version_id ASC;
