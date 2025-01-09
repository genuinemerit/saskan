UPDATE `METADATA` SET
`name_space`=?,
`model_name`=?,
`tbl_name`=?,
`col_name`=?,
`col_def`=?,
`delete_ts`=?
WHERE `meta_uid_pk`=?;
