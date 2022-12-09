-- Запрос для получения uuid исполнителей из КИД
SELECT DISTINCT
    users.name,
    users.id
FROM
    user users
WHERE
    users.delete_ts IS NULL
    AND users.id IN %(kid_executors)s
GROUP BY
    users.name,
    users.id
ORDER BY
    users.name