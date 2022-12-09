SELECT
    org_name,
    inbox,
    outbox,
    signed,
    ROUND(
        CAST(
            CAST(signed AS FLOAT) / (CAST(NULLIF(outbox, 0) AS FLOAT)) * 100 AS NUMERIC
        ),
        2
    ) signed_percent
FROM
    (
        SELECT
            DISTINCT org_names.org_name AS org_name,
            coalesce(inbox._count, 0) AS inbox,
            coalesce(outbox._count, 0) AS outbox,
            coalesce(signed._count, 0) AS signed
        FROM
            (
                SELECT
                    org.name AS org_name
                FROM
                    org org
                WHERE
                    org.name not in %(excluded_organizations)s
                    AND org.delete_ts IS NULL
            ) AS org_names
            LEFT JOIN (
                -- Входящие
                SELECT
                    org.name AS org_name,
                    COUNT(DISTINCT ofdata.id) as _count
                FROM
                    doc document
                    LEFT JOIN doc_data ofdata ON document.card_id = ofdata.doc_id
                    LEFT JOIN org org ON org.id = document.organization_id
                WHERE
                    document.doc_kind_id = 'uuid_doc_income' -- UUID входящих
                    AND document.reg_date >= %(date_start)s
                    AND document.reg_date <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
                    AND ofdata.delete_ts IS NULL
                GROUP BY
                    org.name
            ) as inbox ON org_names.org_name = inbox.org_name
            LEFT JOIN (
                -- Исходящие
                SELECT DISTINCT
                    org.name AS org_name,
                    COUNT(document.card_id) AS _count
                FROM
                    doc document
                    LEFT JOIN doc_data ddod ON document.card_id = ddod.doc_id
                    LEFT JOIN org org ON document.organization_id = org.id
                WHERE
                    document.doc_kind_id = 'uuid_doc_outcome' -- UUID исходящих
                    AND document.reg_date >= %(date_start)s
                    AND document.reg_date <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
                    AND ddod.delete_ts IS NULL
                GROUP BY
                    org.name
            ) AS outbox ON outbox.org_name = org_names.org_name
            LEFT JOIN (
                -- Подписанные
                SELECT
                    org.name AS org_name,
                    COUNT(DISTINCT ofdata.id) AS _count
                FROM
                    doc document
                    LEFT JOIN doc_data ofdata ON document.card_id = ofdata.doc_id
                    LEFT JOIN wf_attachment wfa ON document.card_id = wfa.card_id
                    LEFT JOIN org org ON document.organization_id = org.id
                WHERE
                    document.reg_date >= %(date_start)s
                    AND document.reg_date <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
                    AND document.doc_kind_id = 'uuid_doc_outcome' -- UUID исходящих
                    AND wfa.signatures IS NOT NULL
                    AND ofdata.delete_ts IS NULL
                GROUP BY
                    org_name
            ) AS signed ON org_names.org_name = signed.org_name
        GROUP BY
            inbox,
            outbox,
            signed,
            org_names.org_name
        ORDER BY
            outbox DESC,
            signed DESC,
            inbox DESC
    ) AS output_data