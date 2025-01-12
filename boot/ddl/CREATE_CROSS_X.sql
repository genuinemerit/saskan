CREATE TABLE IF NOT EXISTS CROSS_X (
cross_x_uid_pk TEXT DEFAULT '',
uid_1_table TEXT DEFAULT '',
uid_1_vfk TEXT DEFAULT '',
uid_2_table TEXT DEFAULT '',
uid_2_vfk TEXT DEFAULT '',
touch_type TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (touch_type IN ('', 'contains', 'is_contained_by', 'borders', 'overlaps', 'informs', 'layers_above', 'layers_below')),
PRIMARY KEY (cross_x_uid_pk));
