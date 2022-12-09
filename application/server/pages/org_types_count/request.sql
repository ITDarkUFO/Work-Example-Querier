SELECT
    CASE
        WHEN dfo.organization_type_id = '4e7ae7f9-63a1-458d-8a2b-31555897cb9d' THEN 'ОИВ'
        WHEN dfo.organization_type_id = '29df8958-5d16-44e9-804c-94f92585a801' THEN 'ФОИВ'
        WHEN dfo.organization_type_id = 'c6fefae3-6c60-4855-9d89-e5bf2ae7c33e' THEN 'ОМСУ'
        WHEN dfo.organization_type_id = '381322a8-7e19-4fb1-9720-170c7f6b9c0d' THEN 'Правительство'
        WHEN dfo.organization_type_id = 'd6d0fda0-e030-0b8c-b8c3-5fb0ca81510d' THEN 'Подвед ОИВ'
        WHEN dfo.organization_type_id = '85dac2ec-1302-5823-dec2-3e0dd6910351' THEN 'Подвед ОМСУ'
        WHEN dfo.organization_type_id = 'd9b32d5b-2533-5447-9e28-14ca1a1e4c52' THEN 'Системные'
        WHEN dfo.organization_type_id IS NULL THEN 'Другое'
    END,
    COUNT(*)
FROM
    org dfo
WHERE
    dfo.name not in %(excluded_organizations)s
    AND dfo.delete_ts IS NULL
GROUP BY
    dfo.organization_type_id
ORDER BY
    dfo.organization_type_id