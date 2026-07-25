"""SQLite 持久化：查询历史与用户收藏"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS query_log (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT, result TEXT, created_at TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS favorites (id INTEGER PRIMARY KEY AUTOINCREMENT, scenario_id INTEGER, created_at TEXT)")
    conn.commit()
    return conn


def log_query(query: str, result_summary: str):
    conn = _get_conn()
    conn.execute("INSERT INTO query_log (query, result, created_at) VALUES (?, ?, ?)",
                 (query, result_summary[:500], datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_history(limit: int = 20):
    conn = _get_conn()
    rows = conn.execute("SELECT query, result, created_at FROM query_log ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [{"query": r[0], "result": r[1], "time": r[2]} for r in rows]
