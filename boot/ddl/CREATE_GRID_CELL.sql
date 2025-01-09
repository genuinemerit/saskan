CREATE TABLE IF NOT EXISTS GRID_CELL (
grid_cell_uid_pk TEXT DEFAULT '',
grid_uid_fk TEXT DEFAULT '',
grid_name TEXT DEFAULT '',
grid_cell_name TEXT DEFAULT '',
x_col_ix INTEGER DEFAULT 0,
y_row_ix INTEGER DEFAULT 0,
z_up_down_ix INTEGER DEFAULT 0,
grid_cell_id TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
FOREIGN KEY (grid_uid_fk) REFERENCES GRID(grid_uid_pk) ON DELETE CASCADE,PRIMARY KEY (grid_cell_uid_pk));
