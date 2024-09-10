CREATE TABLE IF NOT EXISTS CHAR_MEMBER (
char_member_uid_pk TEXT DEFAULT '',
char_set_uid_fk TEXT DEFAULT '',
char_member_name TEXT DEFAULT '',
char_member_uri TEXT DEFAULT '',
char_member_desc TEXT DEFAULT '',
delete_dt TEXT DEFAULT '',
FOREIGN KEY (char_set_uid_fk) REFERENCES CHAR_SET(char_set_uid_pk) ON DELETE CASCADE,
PRIMARY KEY (char_member_uid_pk));
