SELECT
    document_data.card_id,
    document_data.reg_no,
    document_data.theme,
    MIN(start_time),
    MAX(finish_time),
    COALESCE(
        MAX(finish_time) - MIN(start_time),
        NOW() :: timestamp - MIN(start_time)
    )
FROM
    (
        SELECT
            document.card_id,
            a.finished AS finish_time
        FROM
            doc document
            LEFT JOIN card c ON c.id = document.card_id
            LEFT JOIN assignment a ON a.card_id = c.id
            LEFT JOIN doc_data ddod ON document.card_id = ddod.doc_id
            LEFT JOIN org ON org.id = document.organization_id
        WHERE
            document.doc_kind_id = 'uuid_doc_income'
            AND ddod.create_ts >= %(date_start)s
            AND ddod.create_ts <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
            AND a.outcome = 'Complete'
            AND a.name = 'ResolutionCreation'
            AND org.name = %(organization_name)s
            AND reg_no IS NOT NULL
            AND c.state NOT LIKE '%%Canceled%%'
    ) AS documents_with_resolutions
    FULL OUTER JOIN (
        SELECT
            document.card_id,
            document.reg_no,
            document.theme,
            a.create_ts AS start_time
        FROM
            doc document
            LEFT JOIN card c ON c.id = document.card_id
            LEFT JOIN assignment a ON a.card_id = c.id
            LEFT JOIN doc_data ddod ON document.card_id = ddod.doc_id
            LEFT JOIN org ON org.id = document.organization_id
        WHERE
            document.doc_kind_id = 'uuid_doc_income'
            AND ddod.create_ts >= %(date_start)s
            AND ddod.create_ts <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
            AND a.outcome != 'CancelRegister'
            AND org.name = %(organization_name)s
            AND reg_no IS NOT NULL
            AND c.state NOT LIKE '%%Canceled%%'
        ORDER BY
            a.create_ts
    ) AS document_data ON document_data.card_id = documents_with_resolutions.card_id
GROUP BY
    document_data.card_id,
    document_data.reg_no,
    document_data.theme
ORDER BY
    MIN(start_time)