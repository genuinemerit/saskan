SELECT `frame_uid_pk`,
`lang_code`,
`frame_id`,
`frame_name`,
`frame_desc`,
`frame_w`,
`frame_h`,
`pg_hdr_x`,
`pg_hdr_y`,
`pg_hdr_w`,
`pg_hdr_h`,
`pg_hdr_txt`,
`delete_dt`
FROM `FRAMES`
ORDER BY `frame_id` ASC;
