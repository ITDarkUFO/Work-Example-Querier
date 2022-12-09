SELECT
    task_data.card_id,
    task_data.task_name,
    task_data.full_descr,
    task_data.create_datetime,
    task_data.finish_datetime_plan,
    executor.name,
    initiator.name
FROM
    task task_data
    LEFT JOIN card wc ON wc.id = task_data.card_id
    LEFT JOIN user executor ON executor.id = task_data.executor_id
    LEFT JOIN user initiator ON initiator.id = task_data.initiator_id
    LEFT JOIN task_user tp ON tp.task_id = task_data.card_id
    AND tp.participant_role = '01-executor'
WHERE
    task_data.num = CONCAT('TM-', %(assignment_number)s)
    AND task_data.primary_task_id IS NULL
    AND wc.delete_ts IS NULL