UPDATE LANG_DIALECT SET
lang_uid_fk=?,
dialect_name=?,
dialect_desc=?,
divergence_factors=?,
syncretic_factors=?,
preservation_factors=?
WHERE dialect_uid_pk=?;
