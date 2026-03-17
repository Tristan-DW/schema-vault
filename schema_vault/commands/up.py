import os
from pathlib import Path
from .base import get_connection, ensure_lock_table, get_applied, record_migration


def run(config: dict, dry_run: bool = False):
    conn = get_connection(config)
    ensure_lock_table(conn, config)

    applied = set(get_applied(conn, config))
    migrations_dir = Path(config.get("migrations_dir", "./migrations"))

    files = sorted(f for f in migrations_dir.glob("*.sql"))
    pending = [f for f in files if f.name not in applied]

    if not pending:
        print("Nothing to migrate - all up to date.")
        return

    for f in pending:
        content = f.read_text()
        parts = content.split("-- down")
        up_sql = parts[0].replace("-- up", "").strip()

        if dry_run:
            print(f"[dry-run] {f.name}:")
            print(up_sql)
            print()
            continue

        cur = conn.cursor()
        try:
            cur.execute(up_sql)
            conn.commit()
            record_migration(conn, config, f.name)
            print(f"Applied: {f.name}")
        except Exception as e:
            conn.rollback()
            print(f"Failed: {f.name} - {e}")
            raise
        finally:
            cur.close()

    conn.close()
