SELECT
    parent.name,
	dfo.name
FROM
    org dfo
LEFT JOIN org parent ON parent.id = dfo.parent_organization_id
WHERE
    dfo.name not in %(excluded_organizations)s
    AND dfo.delete_ts is NULL
ORDER BY
    parent.name NULLS FIRST