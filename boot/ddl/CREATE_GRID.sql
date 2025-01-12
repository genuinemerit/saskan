CREATE TABLE IF NOT EXISTS GRID (
grid_uid_pk TEXT DEFAULT '',
grid_id TEXT DEFAULT '',
x_col_cnt INTEGER DEFAULT 0,
y_row_cnt INTEGER DEFAULT 0,
z_up_cnt INTEGER DEFAULT 0,
z_down_cnt INTEGER DEFAULT 0,
delete_dt TEXT DEFAULT '',
PRIMARY KEY (grid_uid_pk));
