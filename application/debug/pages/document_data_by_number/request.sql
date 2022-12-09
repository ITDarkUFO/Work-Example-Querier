SELECT
    document_data.card_id,
    document_data.theme,
    MIN(start_time),
    MAX(finish_time),
    COALESCE(
        MAX(finish_time) - MIN(start_time),
        NOW() :: timestamp - MIN(start_time)
    ),
    org_name
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
        WHERE
            document.doc_kind_id = 'uuid_doc_income'
            AND a.outcome = 'Complete'
            AND a.name = 'ResolutionCreation'
            AND reg_no = %(document_number)s
    ) AS documents_with_resolutions
    FULL OUTER JOIN (
        SELECT
            document.card_id,
            document.theme,
            a.create_ts AS start_time,
            org.name AS org_name
        FROM
            doc document
            LEFT JOIN card c ON c.id = document.card_id
            LEFT JOIN assignment a ON a.card_id = c.id
            LEFT JOIN doc_data ddod ON document.card_id = ddod.doc_id
            LEFT JOIN org ON org.id = document.organization_id
        WHERE
            document.doc_kind_id = 'uuid_doc_income'
            AND a.outcome != 'CancelRegister'
            AND reg_no = %(document_number)s
        ORDER BY
            a.create_ts
    ) AS document_data ON document_data.card_id = documents_with_resolutions.card_id
GROUP BY
    org_name,
    document_data.card_id,
    document_data.theme
ORDER BY
    org_name,
    MIN(start_time)
    