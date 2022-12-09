SELECT
    org_name,
    COALESCE(sum(CASE
        WHEN transit_time < INTERVAL %(time_interval)s
        THEN 1
        ELSE 0 END), 0),

    COALESCE(sum(CASE
        WHEN transit_time >= INTERVAL %(time_interval)s
        THEN 1
        ELSE 0 END), 0)
FROM
    (
        SELECT
            org_name,
            COALESCE(
                MAX(finish_time) - MIN(start_time),
                NOW() :: timestamp - MIN(start_time)
            ) AS transit_time
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
                    AND ddod.create_ts >= %(date_start)s
                    AND ddod.create_ts <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
                    AND a.outcome = 'Complete'
                    AND a.name = 'ResolutionCreation'
                    AND reg_no IS NOT NULL
                    AND c.state NOT LIKE '%%Canceled%%'
            ) AS documents_with_resolutions
            FULL OUTER JOIN (
                SELECT
                    org.name AS org_name,
                    document.card_id,
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
                    AND reg_no IS NOT NULL
                    AND c.state NOT LIKE '%%Canceled%%'
                ORDER BY
                    a.create_ts
            ) AS document_data ON document_data.card_id = documents_with_resolutions.card_id
        GROUP BY
            document_data.card_id,
            document_data.org_name
    ) AS document_full_data
GROUP BY
    document_full_data.org_name
ORDER BY
    document_full_data.org_name