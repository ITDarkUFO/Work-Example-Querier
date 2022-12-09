SELECT
    task_data.card_id,
    task_data.num,
    CASE
        WHEN LENGTH(task_data.task_name) > 150
        THEN CONCAT(LEFT(task_data.task_name, 150), '...')
        ELSE task_data.task_name
    END,
    CASE
        WHEN LENGTH(task_data.full_descr) > 300
        THEN CONCAT(LEFT(task_data.full_descr, 300), '...')
        ELSE task_data.full_descr
    END,
    task_data.create_datetime,
    task_data.finish_datetime_plan,
    initiator.name,
    STRING_AGG(controller.name, ', ')
FROM
    task task_data
    LEFT JOIN user executor ON executor.id = task_data.executor_id
    LEFT JOIN user initiator ON initiator.id = task_data.initiator_id
    LEFT JOIN task_user tp ON tp.task_id = task_data.card_id
    AND tp.participant_role = '01-executor'
    LEFT JOIN card wc ON wc.id = task_data.card_id
    LEFT JOIN card_role cr ON cr.card_id = task_data.card_id
    LEFT JOIN user controller ON controller.id = cr.user_id
WHERE
    (
        finish_date_plan >= %(date_start)s
        AND finish_date_plan <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
        AND wc.delete_ts IS NULL
        AND wc.state NOT LIKE '%%Canceled%%'
        AND task_data.primary_task_id IS NULL
        AND executor.id IN (%(executor_input)s)
        AND cr.code = '30-Controller'
        AND task_data.initiator_id IN %(initiators_list)s
        AND execution_datetime IS NULL
    )
GROUP BY
    task_data.card_id,
    task_data.num,
    task_data.task_name,
    task_data.full_descr,
    task_data.create_datetime,
    task_data.finish_datetime_plan,
    initiator.name
ORDER BY
    task_data.finish_datetime_plan ASC,
    task_data.create_datetime
