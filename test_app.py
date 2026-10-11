import unittest,tempfile,sqlite3
from pathlib import Path
import app
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'test.db';app.build(self.path)
 def tearDown(self):self.tmp.cleanup()
 def test_totals(self):
  s=app.report(self.path)['01_portfolio'][0];self.assertEqual(s['projects'],180);self.assertEqual(s['completed'],160);self.assertEqual(s['active'],20)
 def test_no_join_multiplication(self):
  with app.connect(self.path) as db:
   self.assertEqual(db.execute('SELECT SUM(cost_cents) FROM project_metrics').fetchone()[0],db.execute('SELECT SUM(amount_cents) FROM expenses').fetchone()[0]);self.assertEqual(db.execute('SELECT COUNT(*) FROM project_metrics').fetchone()[0],180)
 def test_foreign_keys(self):
  with app.connect(self.path) as db:
   with self.assertRaises(sqlite3.IntegrityError):db.execute("INSERT INTO expenses(project_id,category,amount_cents) VALUES (999,'Other',1)")
 def test_completed_only_delays(self):
  rows=app.report(self.path)['02_delayed_projects'];self.assertTrue(rows);self.assertTrue(all(r['delay_days']>0 and r['actual_finish'] for r in rows))
 def test_window_total(self):
  rows=app.report(self.path)['06_monthly_trends'];self.assertEqual(rows[-1]['cumulative_completed'],160);self.assertIsNone(rows[0]['change_in_completed'])
 def test_pending_permits(self):
  rows=app.report(self.path)['05_permit_analysis'];self.assertEqual(sum(r['pending_permits'] for r in rows),20)
 def test_no_overwrite(self):
  with self.assertRaises(FileExistsError):app.build(self.path)
if __name__=='__main__':unittest.main()
