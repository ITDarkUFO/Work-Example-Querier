SELECT
    document.card_id,
    document.reg_no,
    document.datetime,
    document.theme,
    document.comment_
FROM
    doc document
    LEFT JOIN doc_data ddod ON document.card_id = ddod.doc_id
    LEFT JOIN org org ON org.id = document.organization_id
WHERE
    document.doc_kind_id = %(doc_type)s
    AND document.reg_date >= %(date_start)s
    AND document.reg_date <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
    AND org.name = %(organization_name)s
    AND ddod.delete_ts IS NULL
GROUP BY
    document.card_id
ORDER BY
    document.datetime