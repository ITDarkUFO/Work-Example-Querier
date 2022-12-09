SELECT
    user_data.id,
    CONCAT(user_data.name, ' (', user_data.login_lc, ')', 
    (CASE WHEN NOT user_data.active
    THEN ' - неактивный'
    END)),
    organization_data.name,
    user_data.position_,
    user_login_data.last_authorization_date
FROM
    user AS user_data
    LEFT JOIN user_deactivation_info AS user_login_data ON user_data.id = user_login_data.user_id
    LEFT JOIN org AS organization_data ON organization_data.id = user_data.organization_id
WHERE
    user_data.delete_ts IS NULL
    AND (user_login_data.last_authorization_date <= NOW() - INTERVAL %(time_interval)s
    OR user_login_data.last_authorization_date IS NULL)
ORDER BY
    user_login_data.last_authorization_date DESC NULLS LAST,
    user_data.active DESC,
    organization_data.name