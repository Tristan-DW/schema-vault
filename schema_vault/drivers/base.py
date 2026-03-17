import sqlite3
import os
from typing import Any


def get_connection(config: dict):
    driver = config.get("driver", "sqlite")
    if driver == "postgres":
        import psycopg2
        return psycopg2.connect(config["connection"])
    elif driver == "mysql":
        import pymysql
        url = config["connection"]
        # Parse mysql://user:pass@host:port/db
        from urllib.parse import urlparse
        p = urlparse(url)
        return pymysql.connect(
            host=p.hostname,
            port=p.port or 3306,
            user=p.username,
            password=p.password,
            database=p.path.lstrip("/"),
            autocommit=False,
        )
    elif driver == "sqlite":
        path = config.get("connection", ":memory:")
        return sqlite3.connect(path)
    else:
        raise ValueError(f"Unsupported driver: {driver}")


def ensure_lock_table(conn, config: dict):
    table = config.get("lock_table", "_schema_vault")
    driver = config.get("driver", "sqlite")
    if driver == "postgres":
        sql = f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id          SERIAL PRIMARY KEY,
                name        VARCHAR(255) UNIQUE NOT NULL,
                applied_at  TIMESTAMPTZ DEFAULT NOW()
            )
        """
    elif driver == "mysql":
        sql = f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                name        VARCHAR(255) UNIQUE NOT NULL,
                applied_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
    else:
        sql = f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT UNIQUE NOT NULL,
                applied_at  TEXT DEFAULT (datetime('now'))
            )
        """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()


def get_applied(conn, config: dict) -> list[dict]:
    table = config.get("lock_table", "_schema_vault")
    cur = conn.cursor()
    cur.execute(f"SELECT name, applied_at FROM {table} ORDER BY id ASC")
    rows = cur.fetchall()
    cur.close()
    return [{"name": r[0], "applied_at": str(r[1])} for r in rows]


def record_migration(conn, config: dict, name: str):
    table = config.get("lock_table", "_schema_vault")
    cur = conn.cursor()
    driver = config.get("driver", "sqlite")
    if driver == "postgres":
        cur.execute(f"INSERT INTO {table} (name) VALUES (%s)", (name,))
    else:
        cur.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
    conn.commit()
    cur.close()


def remove_migration(conn, config: dict, name: str):
    table = config.get("lock_table", "_schema_vault")
    cur = conn.cursor()
    driver = config.get("driver", "sqlite")
    if driver == "postgres":
        cur.execute(f"DELETE FROM {table} WHERE name = %s", (name,))
    else:
        cur.execute(f"DELETE FROM {table} WHERE name = ?", (name,))
    conn.commit()
    cur.close()


def execute_sql(conn, sql: str):
    cur = conn.cursor()
    # Split on semicolons for multi-statement migrations
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    for statement in statements:
        cur.execute(statement)
    conn.commit()
    cur.close()
