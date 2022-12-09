SELECT
    DISTINCT org_names.org_name AS org_name,
    coalesce(inbox._count, 0) AS inbox
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
            COUNT(DISTINCT document.card_id) as _count
        FROM
            doc document
            LEFT JOIN card c ON c.id = document.card_id
            LEFT JOIN assignment a ON a.card_id = c.id
            LEFT JOIN doc_data ofdata ON document.card_id = ofdata.doc_id
            LEFT JOIN org org ON org.id = document.organization_id
        WHERE
            document.doc_kind_id = 'uuid_doc_income' -- UUID входящих
            AND ofdata.create_ts >= %(date_start)s
            AND ofdata.create_ts <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
            AND NOW() :: timestamp - ofdata.create_ts >= INTERVAL %(register_interval)s
            AND c.state NOT LIKE '%%Canceled%%'
            AND reg_no IS NULL
            AND org.delete_ts IS NULL
        GROUP BY
            org.name
    ) as inbox ON org_names.org_name = inbox.org_name
GROUP BY
    inbox,
    org_names.org_name
ORDER BY
    inbox DESC
