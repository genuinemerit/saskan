SELECT `meta_uid_pk`,
`name_space`,
`model_name`,
`tbl_name`,
`col_name`,
`col_def`,
`delete_ts`
FROM `METADATA`
ORDER BY `tbl_name` ASC, `col_name` ASC;
