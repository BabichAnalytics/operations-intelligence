# Operations Intelligence
**Babich Analytics | SQL construction operations portfolio**

Analyze schedules, budgets, permitting and crew throughput with SQLite. All 180 projects are fictional: no Green Shield records or customer information are used. AI assisted implementation; learn and explain the queries before presenting this as evidence of your skills.

## Start on Windows
Python 3.10+; no packages, paid services, or database server required.
Download and extract the repository. Open Command Prompt in the folder:
```cmd
python app.py
```
Open http://127.0.0.1:8004 and keep the terminal open. Ctrl+C stops it.
The first run creates `operations.db`; later runs reuse it.
```cmd
python -m unittest -v
python app.py --report results.json
```
Use `--db new_demo.db` to generate a fresh demo without overwriting an existing database. Export the selected analysis as CSV from the dashboard.

## Data model
`crews` → `projects` → `expenses` (many expense records per project).
`projects` → `permits` (one permit per demo project).
Primary/foreign keys, CHECK constraints and indexes enforce basic integrity. Monetary values use integer cents. `project_metrics` aggregates expense records before joining, preventing double-counted budgets.

## Six SQL analyses
1. Portfolio counts and completed-project late percentage — conditional aggregation and NULLIF.
2. Late completions — date arithmetic and ordering.
3. Completed-project budget variance — integer-cent calculations.
4. Crew throughput — CTE and DENSE_RANK.
5. Permit approval times — LEFT JOIN, NULL handling and grouped summaries.
6. Monthly completions — LAG and cumulative SUM window functions.

Run individual queries with a SQLite client, or inspect the numbered `.sql` files and run them through Python's sqlite3 module. The dashboard executes these same files; SQL is the core analysis, Python handles sample generation and presentation.

## Metric definitions and limits
Late = actual finish after planned finish; open projects excluded from late and budget comparisons. Early finishes contribute zero to average late days. Permit averages exclude pending permits; pending counts remain visible. Monthly change compares adjacent observed completion months, not missing calendar months. Crew rankings count completed projects and do not control for job complexity, hours, staffing, or assignment mix. Spend is not revenue or profit. This synthetic dataset cannot support causal conclusions about permits or actual businesses.

## Learning exercises
Add an expense category breakdown; calculate project duration; introduce multiple permits while preserving one-row-per-project metrics; add missing calendar months to monthly trends; compare project types before interpreting crew performance.

## Files
`schema.sql`: schema and view. Numbered SQL files: business queries. `app.py`: deterministic seed 42 demo and local server. `dashboard.html`: report explorer and CSV export. `test_app.py`: integrity and calculation checks.
