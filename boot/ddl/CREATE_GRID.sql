CREATE TABLE IF NOT EXISTS GRID (
grid_uid_pk TEXT DEFAULT '',
version_id TEXT DEFAULT '',
grid_name TEXT DEFAULT '',
row_cnt INTEGER DEFAULT 0,
col_cnt INTEGER DEFAULT 0,
z_up_cnt INTEGER DEFAULT 0,
z_down_cnt INTEGER DEFAULT 0,
PRIMARY KEY (grid_uid_pk));
