-- Monetary amounts stored as integer cents; dollars are presentation only.
SELECT project_id, crew, ROUND(budget_cents/100.0,2) AS budget,
 ROUND(cost_cents/100.0,2) AS actual_cost,
 ROUND((cost_cents-budget_cents)/100.0,2) AS variance,
 ROUND(100.0*(cost_cents-budget_cents)/budget_cents,1) AS variance_pct
FROM project_metrics WHERE actual_finish IS NOT NULL
ORDER BY variance DESC, project_id;
