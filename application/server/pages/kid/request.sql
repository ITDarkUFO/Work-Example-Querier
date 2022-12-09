SELECT
    owner_id,
    owner_name,
    sum(assignments_count),
    sum(done_on_time_count),
    sum(overdue_assignment_list_count),
    sum(unfinished_count)
FROM
    (
        SELECT
            person.id AS owner_id,
            person.name AS owner_name,
            assignments_count,
            done_on_time_count,
            overdue_assignment_list_count,
            unfinished_count
        FROM
            (
                SELECT DISTINCT
                    person.id,
                    person.name
                FROM
                    user person
                WHERE
                    person.id IN %(kid_executors)s
            ) AS person
            LEFT JOIN (
                SELECT
                    person.name executor_name,
                    sum(
                        CASE
                            WHEN num IS NOT NULL THEN 1
                        END
                    ) assignments_count,
                    (
                        SUM (
                            CASE
                                WHEN execution_datetime <= finish_datetime_plan THEN 1
                            END
                        )
                    ) done_on_time_count,
                    (
                        SUM (
                            CASE
                                WHEN execution_datetime > finish_datetime_plan THEN 1
                            END
                        )
                    ) overdue_assignment_list_count,
                    (
                        SUM (
                            CASE
                                WHEN execution_datetime IS NULL THEN 1
                            END
                        )
                    ) unfinished_count
                FROM
                    task assignment_card
                    LEFT JOIN user person ON person.id = assignment_card.executor_id
                    LEFT JOIN task_user tp ON tp.task_id = assignment_card.card_id
                    AND tp.participant_role = '01-executor'
                    LEFT JOIN card wc ON wc.id = assignment_card.card_id
                WHERE
                    (
                        finish_date_plan >= %(date_start)s
                        AND finish_date_plan <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
                        AND wc.delete_ts IS NULL
                        AND wc.state NOT LIKE '%%Canceled%%'
                        AND assignment_card.primary_task_id IS NULL
                        AND assignment_card.initiator_id IN %(initiators_list)s
                    )
                GROUP BY
                    person.name,
                    assignment_card.finish_datetime_plan,
                    assignment_card.execution_datetime
                ORDER BY
                    person.name
            ) AS assignments ON assignments.executor_name = person.name
    ) assignments
GROUP BY
    owner_id,
    owner_name
ORDER BY
    owner_name
