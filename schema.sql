PRAGMA foreign_keys = ON;
CREATE TABLE crews (crew_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE projects (
 project_id INTEGER PRIMARY KEY, crew_id INTEGER NOT NULL REFERENCES crews,
 project_type TEXT NOT NULL, planned_start TEXT NOT NULL, planned_finish TEXT NOT NULL,
 actual_finish TEXT, budget_cents INTEGER NOT NULL CHECK(budget_cents>0),
 CHECK(planned_finish >= planned_start), CHECK(actual_finish IS NULL OR actual_finish >= planned_start)
);
CREATE TABLE expenses (
 expense_id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES projects,
 category TEXT NOT NULL, amount_cents INTEGER NOT NULL CHECK(amount_cents>=0)
);
CREATE TABLE permits (
 permit_id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL UNIQUE REFERENCES projects,
 submitted TEXT NOT NULL, approved TEXT, CHECK(approved IS NULL OR approved>=submitted)
);
CREATE INDEX expenses_project ON expenses(project_id);
CREATE INDEX projects_crew ON projects(crew_id);
-- Aggregate the many-side BEFORE joining to avoid multiplying project budgets.
CREATE VIEW project_metrics AS
WITH costs AS (SELECT project_id, SUM(amount_cents) AS cost_cents FROM expenses GROUP BY project_id)
SELECT p.*, c.name AS crew, COALESCE(costs.cost_cents,0) AS cost_cents,
 CASE WHEN actual_finish IS NOT NULL THEN CAST(julianday(actual_finish)-julianday(planned_finish) AS INTEGER) END AS delay_days,
 CASE WHEN pe.approved IS NOT NULL THEN CAST(julianday(pe.approved)-julianday(pe.submitted) AS INTEGER) END AS permit_days
FROM projects p JOIN crews c USING(crew_id)
LEFT JOIN costs USING(project_id) LEFT JOIN permits pe USING(project_id);
