SELECT
    fio.id,
    fio.fio as name,
    jsonb_agg(t2."bad/daysoverdue") filter (
        where
            t2."bad/daysoverdue" is not null
    ) as "daysoverdue",
    t2.coefficient
FROM
    (
        SELECT DISTINCT
            su.name fio,
            su.id

        FROM
            user su
            LEFT JOIN employee de ON de.user_id = su.id
            LEFT JOIN position dp ON dp.id = de.position_id
        WHERE
            su.id IN %(kid_executors)s
    ) AS fio
    LEFT JOIN (
        SELECT
            su."name" fio,
            COUNT(tt.card_id) quantity,
            (
                CASE
                    WHEN gtk.name IN %(assignments_sources_1)s THEN 1
                    WHEN gtk.name IN %(assignments_sources_2)s THEN 2
                    WHEN gtk.name IN %(assignments_sources_3)s THEN 3
                END
            ) coefficient,
            (
                CASE
                    WHEN (
                        SUM (
                            CASE
                                WHEN execution_datetime > finish_datetime_plan THEN 1
                                ELSE 0
                            END
                        )
                    ) != 0 THEN CONCAT_WS(
                        '/',
                        (
                            SUM (
                                CASE
                                    WHEN execution_datetime > finish_datetime_plan THEN 1
                                END
                            )
                        ),
                        CASE
                            WHEN (
                                date_part(
                                    'day',
                                    (execution_datetime - finish_datetime_plan)
                                )
                            ) = 0 THEN 1
                            ELSE (
                                date_part(
                                    'day',
                                    (execution_datetime - finish_datetime_plan)
                                )
                            )
                        END
                    )
                END
            ) as "bad/daysoverdue"
        FROM
            task tt
            LEFT JOIN task_kind gtk ON gtk.id = tt.task_kind
            LEFT JOIN user su ON su.id = tt.executor_id
            LEFT JOIN task_user tp ON tp.task_id = tt.card_id
            AND tp.participant_role = '01-executor'
            LEFT JOIN employee de ON de.user_id = su.id
            LEFT JOIN position dp ON dp.id = de.position_id
            JOIN card wc ON wc.id = tt.card_id
        WHERE
            (
                finish_date_plan >= %(date_start)s
                AND finish_date_plan <= %(date_end)s :: DATE + INTERVAL '23 HOUR 59 MINUTE'
                AND wc.delete_ts IS NULL
                AND tt.primary_task_id IS NULL
                AND tt.initiator_id IN %(initiators_list)s
            )
        GROUP BY
            su.name,
            gtk.name,
            tt.finish_datetime_plan,
            tt.execution_datetime
        ORDER BY
            su.name,
            coefficient asc
    ) AS t2 ON t2.fio = fio.fio
GROUP BY
    fio.id,
    fio.fio,
    t2.coefficient
ORDER BY
    fio.fio