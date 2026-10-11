-- Completion month; LAG demonstrates change from previous observed completion month.
WITH monthly AS (
 SELECT substr(actual_finish,1,7) AS month, COUNT(*) AS completed,
 ROUND(SUM(cost_cents)/100.0,2) AS cost
 FROM project_metrics WHERE actual_finish IS NOT NULL GROUP BY month
)
SELECT *, completed-LAG(completed) OVER(ORDER BY month) AS change_in_completed,
 SUM(completed) OVER(ORDER BY month ROWS UNBOUNDED PRECEDING) AS cumulative_completed
FROM monthly ORDER BY month;
