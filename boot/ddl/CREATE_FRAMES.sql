CREATE TABLE IF NOT EXISTS FRAMES (
frame_uid_pk TEXT DEFAULT '',
lang_code TEXT DEFAULT '',
frame_id TEXT DEFAULT '',
frame_name TEXT DEFAULT '',
frame_desc TEXT DEFAULT '',
frame_w NUMERIC DEFAULT 0.0,
frame_h NUMERIC DEFAULT 0.0,
pg_hdr_x NUMERIC DEFAULT 0.0,
pg_hdr_y NUMERIC DEFAULT 0.0,
pg_hdr_w NUMERIC DEFAULT 0.0,
pg_hdr_h NUMERIC DEFAULT 0.0,
pg_hdr_txt TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (lang_code IN ('en')),
PRIMARY KEY (frame_uid_pk));
