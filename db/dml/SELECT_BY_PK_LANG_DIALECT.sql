SELECT dialect_uid_pk, lang_uid_fk, dialect_name, dialect_desc, divergence_factors, syncretic_factors, preservation_factors
FROM LANG_DIALECT
WHERE dialect_uid_pk=?
ORDER BY dialect_name ASC;
