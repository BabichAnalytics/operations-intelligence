-- Counts measure throughput, not crew productivity: project complexity/hours are not controlled.
WITH crew_summary AS (
 SELECT crew, COUNT(*) AS assigned, SUM(actual_finish IS NOT NULL) AS completed,
 ROUND(AVG(CASE WHEN actual_finish IS NOT NULL THEN MAX(delay_days,0) END),1) AS avg_late_days
 FROM project_metrics GROUP BY crew
)
SELECT *, DENSE_RANK() OVER(ORDER BY completed DESC) AS completion_rank
FROM crew_summary ORDER BY completion_rank, crew;
