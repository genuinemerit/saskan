CREATE TABLE IF NOT EXISTS WINDOWS (
win_uid_pk TEXT DEFAULT '',
frame_uid_fk TEXT DEFAULT '',
frame_id TEXT DEFAULT '',
lang_code TEXT DEFAULT '',
version_id TEXT DEFAULT '',
win_id TEXT DEFAULT '',
win_title TEXT DEFAULT '',
win_margin NUMERIC DEFAULT 0.0,
CHECK (lang_code IN ('en')),
FOREIGN KEY (frame_uid_fk) REFERENCES FRAMES(frame_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (win_uid_pk));
