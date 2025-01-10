CREATE TABLE IF NOT EXISTS GRID_INFO (
grid_info_uid_pk TEXT DEFAULT '',
grid_uid_fk TEXT DEFAULT '',
grid_cell_uid_fk TEXT DEFAULT '',
grid_name TEXT DEFAULT '',
grid_cell_name TEXT DEFAULT '',
grid_info_id TEXT DEFAULT '',
grid_info_data_type TEXT DEFAULT '',
grid_info_name TEXT DEFAULT '',
grid_info_value BLOB DEFAULT 'b''',
grid_info_path TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (grid_info_data_type IN ('TEXT', 'INT', 'FLOAT', 'JSON', 'BLOB')),
FOREIGN KEY (grid_cell_uid_fk) REFERENCES GRID_CELL(grid_cell_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (grid_uid_fk) REFERENCES GRID(grid_uid_pk) ON DELETE CASCADE,PRIMARY KEY (grid_info_uid_pk));