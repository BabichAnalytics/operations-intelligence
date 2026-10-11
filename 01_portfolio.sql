-- One row per project; cost is spend to date. Budget comparisons use completed projects only.
SELECT COUNT(*) AS projects,
 SUM(actual_finish IS NOT NULL) AS completed,
 SUM(actual_finish IS NULL) AS active,
 SUM(CASE WHEN delay_days>0 THEN 1 ELSE 0 END) AS late_completed,
 ROUND(100.0*SUM(CASE WHEN delay_days>0 THEN 1 ELSE 0 END)/NULLIF(SUM(actual_finish IS NOT NULL),0),1) AS late_pct,
 SUM(CASE WHEN actual_finish IS NOT NULL AND cost_cents>budget_cents THEN 1 ELSE 0 END) AS over_budget_completed
FROM project_metrics;
