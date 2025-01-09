UPDATE `LUNAR_CALENDAR` SET
`lunar_year_uid_fk`=?,
`lunar_year_name_gloss_common_uid_vfk`=?,
`lunar_calendar_name`=?,
`lunar_calendar_desc`=?,
`epoch_start_offset`=?,
`days_in_month`=?,
`delete_dt`=?
WHERE `lunar_calendar_uid_pk`=?;
