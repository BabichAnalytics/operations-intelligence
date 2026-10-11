-- Approved permits only; pending permits reported separately.
SELECT project_type, COUNT(*) AS projects,
 COUNT(permit_days) AS approved_permits,
 SUM(permit_days IS NULL) AS pending_permits,
 ROUND(AVG(permit_days),1) AS avg_approval_days,
 ROUND(AVG(CASE WHEN permit_days IS NOT NULL AND actual_finish IS NOT NULL THEN MAX(delay_days,0) END),1) AS avg_late_days_for_approved_completed
FROM project_metrics GROUP BY project_type ORDER BY project_type;
