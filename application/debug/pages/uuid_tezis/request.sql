-- Запрос для получения uuid пользователей
SELECT DISTINCT
    users.name,
    users.id
FROM
    user users
WHERE
    users.delete_ts IS NULL
ORDER BY
    users.name