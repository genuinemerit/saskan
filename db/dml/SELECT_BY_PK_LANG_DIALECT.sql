SELECT dialect_uid_pk, lang_uid_fk, dialect_name, dialect_desc, divergence_factors, syncretic_factors, preservation_factors, delete_dt
FROM LANG_DIALECT
WHERE d=? AND i=? AND a=? AND l=? AND e=? AND c=? AND t=? AND _=? AND u=? AND i=? AND d=? AND _=? AND p=? AND k=?
ORDER BY dialect_name ASC;
