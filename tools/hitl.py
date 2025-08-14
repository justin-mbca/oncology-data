#HITL queue (SQLite-backed)
import sqlite3, json, time
from common.schemas import HITLArgs, ToolResult
from common.settings import settings

def _conn():
    con = sqlite3.connect(settings.HITL_DB)
    con.execute("""CREATE TABLE IF NOT EXISTS tasks(
      id TEXT PRIMARY KEY, created_ts REAL, summary TEXT, diffs TEXT, status TEXT
    )""")
    return con

def hitl_queue(args: HITLArgs) -> ToolResult:
    con = _conn()
    con.execute("INSERT OR REPLACE INTO tasks VALUES (?,?,?,?,?)",
                (args.task_id, time.time(), args.summary, args.diffs or "", "PENDING"))
    con.commit(); con.close()
    return ToolResult(ok=True, data={"task_id": args.task_id, "status": "PENDING"})

def hitl_decide(task_id: str, approve: bool) -> ToolResult:
    con = _conn()
    con.execute("UPDATE tasks SET status=? WHERE id=?", ("APPROVED" if approve else "REJECTED", task_id))
    con.commit(); con.close()
    return ToolResult(ok=True, data={"task_id": task_id, "status": "APPROVED" if approve else "REJECTED"})
