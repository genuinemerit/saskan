INSERT INTO `LUNAR_CALENDAR` (
`lunar_calendar_uid_pk`,
`lunar_year_uid_fk`,
`lunar_year_name_gloss_common_uid_vfk`,
`lunar_calendar_name`,
`lunar_calendar_desc`,
`epoch_start_offset`,
`days_in_month`,
`delete_dt`) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
