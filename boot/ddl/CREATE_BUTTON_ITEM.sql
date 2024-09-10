CREATE TABLE IF NOT EXISTS BUTTON_ITEM (
button_item_uid_pk TEXT DEFAULT '',
button_multi_uid_fk TEXT DEFAULT '',
button_name TEXT DEFAULT '',
button_icon TEXT DEFAULT '',
button_order INTEGER DEFAULT 0,
button_action TEXT DEFAULT '',
is_enabled BOOLEAN DEFAULT 1,
help_text TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
FOREIGN KEY (button_multi_uid_fk) REFERENCES BUTTON_MULTI(button_multi_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (button_item_uid_pk));
