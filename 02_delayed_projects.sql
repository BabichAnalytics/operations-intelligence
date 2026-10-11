-- Positive delay = completed after planned finish. Open projects excluded.
SELECT project_id, crew, project_type, planned_finish, actual_finish, delay_days
FROM project_metrics WHERE delay_days>0
ORDER BY delay_days DESC, project_id;
