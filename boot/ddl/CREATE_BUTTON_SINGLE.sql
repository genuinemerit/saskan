CREATE TABLE IF NOT EXISTS BUTTON_SINGLE (
button_single_uid_pk TEXT DEFAULT '',
button_type TEXT DEFAULT '',
button_name TEXT DEFAULT '',
button_icon TEXT DEFAULT '',
button_key TEXT DEFAULT '',
frame_uid_fk TEXT DEFAULT '',
window_uid_fk TEXT DEFAULT '',
x NUMERIC DEFAULT 0.0,
y NUMERIC DEFAULT 0.0,
enabled BOOLEAN DEFAULT 1,
help_text TEXT DEFAULT '',
action TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (button_type IN ('toggle', 'check', 'radio', 'event')),
FOREIGN KEY (frame_uid_fk) REFERENCES FRAMES(frame_uid_pk) ON DELETE CASCADE,
FOREIGN KEY (window_uid_fk) REFERENCES WINDOWS(window_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (button_single_uid_pk));
