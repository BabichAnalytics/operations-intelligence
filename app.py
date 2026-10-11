"""Reproducible SQLite construction analytics. Python standard library only."""
import argparse, json, random, sqlite3
from datetime import date, timedelta
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
ROOT=Path(__file__).resolve().parent
QUERIES=sorted(ROOT.glob('[0-9][0-9]_*.sql'))
def connect(path):
    db=sqlite3.connect(path); db.row_factory=sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON'); return db

def build(path):
    # Refuse to overwrite an existing database.
    if Path(path).exists(): raise FileExistsError(f'{path} already exists; choose a new --db path')
    db=connect(path); db.executescript((ROOT/'schema.sql').read_text())
    rng=random.Random(42)
    with db:
        db.executemany('INSERT INTO crews VALUES (?,?)',enumerate(['Cedar','Maple','Oak','Pine'],1))
        for i in range(1,181):
            start=date(2025,1,1)+timedelta(days=rng.randrange(300)); finish=start+timedelta(days=rng.randint(5,25))
            delay=rng.choice([-3,0,0,2,5,10]); actual=None if i%9==0 else (finish+timedelta(days=delay)).isoformat()
            budget=rng.randint(80,350)*10000
            db.execute('INSERT INTO projects VALUES (?,?,?,?,?,?,?)',(i,rng.randint(1,4),rng.choice(['Deck','Patio','Addition']),start.isoformat(),finish.isoformat(),actual,budget))
            total=budget*rng.randint(75,125)//100
            if actual is None: total=total//2
            material=total*60//100; labor=total*35//100
            db.executemany('INSERT INTO expenses(project_id,category,amount_cents) VALUES (?,?,?)',[(i,'Materials',material),(i,'Labor',labor),(i,'Other',total-material-labor)])
            submitted=start-timedelta(days=25); approved=None if actual is None else (submitted+timedelta(days=rng.randint(3,30))).isoformat()
            db.execute('INSERT INTO permits(project_id,submitted,approved) VALUES (?,?,?)',(i,submitted.isoformat(),approved))
    db.close()

def report(path):
    with connect(path) as db:
        return {q.stem:[dict(r) for r in db.execute(q.read_text())] for q in QUERIES}

class Handler(BaseHTTPRequestHandler):
    data=None
    def do_GET(self):
        if self.path=='/': body=(ROOT/'dashboard.html').read_bytes(); mime='text/html; charset=utf-8'
        elif self.path=='/api/report': body=json.dumps(self.data).encode(); mime='application/json'
        else: self.send_error(404); return
        self.send_response(200); self.send_header('Content-Type',mime); self.send_header('Content-Length',str(len(body))); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body)

def main():
    a=argparse.ArgumentParser(); a.add_argument('--db',type=Path,default=ROOT/'operations.db'); a.add_argument('--report',type=Path); a.add_argument('--port',type=int,default=8004); args=a.parse_args()
    if not args.db.exists(): build(args.db)
    result=report(args.db)
    if args.report: args.report.write_text(json.dumps(result,indent=2)); print('Saved',args.report); return
    Handler.data=result
    with ThreadingHTTPServer(('127.0.0.1',args.port),Handler) as server:
        print(f'Open http://127.0.0.1:{args.port} — Ctrl+C to stop',flush=True)
        try: server.serve_forever()
        except KeyboardInterrupt: pass
if __name__=='__main__': main()
