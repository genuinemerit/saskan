CREATE TABLE IF NOT EXISTS CHAR_SET (
char_set_uid_pk TEXT DEFAULT '',
font_name TEXT DEFAULT '',
char_set_type TEXT DEFAULT 'alphabet',
char_set_desc TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
CHECK (char_set_type IN ('alphabet', 'abjad', 'abugida', 'syllabary', 'ideogram')),
PRIMARY KEY (char_set_uid_pk));
