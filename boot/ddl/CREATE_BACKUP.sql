CREATE TABLE IF NOT EXISTS BACKUP (
bkup_uid_pk TEXT DEFAULT '',
bkup_id TEXT DEFAULT '',
bkup_dttm TEXT DEFAULT '',
bkup_type TEXT DEFAULT '',
file_from TEXT DEFAULT '',
file_to TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (bkup_type IN ('archive', 'backup', 'compressed', 'export', 'encrypted')),
PRIMARY KEY (bkup_uid_pk));
