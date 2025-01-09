CREATE TABLE IF NOT EXISTS METADATA (
meta_uid_pk TEXT DEFAULT '',
name_space TEXT DEFAULT '',
model_name TEXT DEFAULT '',
tbl_name TEXT DEFAULT '',
col_name TEXT DEFAULT '',
col_def TEXT DEFAULT '',
delete_ts TEXT DEFAULT '',
CHECK (name_space IN ('app', 'story')),
PRIMARY KEY (meta_uid_pk));
