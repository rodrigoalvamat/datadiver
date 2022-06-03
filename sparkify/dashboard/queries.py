songplays_by_user = """
SELECT COUNT(*) AS plays, CONCAT(u.first_name, ' ', u.last_name) AS user, u.gender, u.level
FROM songplays AS s
JOIN users AS u
ON s.user_id = u.user_id
GROUP BY s.user_id, u.first_name, u.last_name, u.gender, u.level
ORDER BY plays DESC;
"""
