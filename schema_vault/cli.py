#!/usr/bin/env python3
"""Schema Vault - Database migration CLI"""
import argparse
import os
import sys
from pathlib import Path

from .commands import init, create, up, down, status
from .config import load_config


def main():
    parser = argparse.ArgumentParser(
        prog="sv",
        description="schema-vault - database migration CLI",
    )
    parser.add_argument("--version", action="version", version="1.0.0")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Initialize a new project").add_argument(
        "name", nargs="?", default="."
    )

    sub.add_parser("create", help="Create a new migration").add_argument("name")

    up_p = sub.add_parser("up", help="Apply pending migrations")
    up_p.add_argument("--dry-run", action="store_true")

    down_p = sub.add_parser("down", help="Roll back migrations")
    down_p.add_argument("--steps", type=int, default=1)

    sub.add_parser("status", help="Show migration status")
    sub.add_parser("reset", help="Drop and re-apply all migrations (dev only)")

    args = parser.parse_args()

    try:
        if args.command == "init":
            init.run(getattr(args, "name", "."))
        elif args.command == "create":
            create.run(args.name)
        elif args.command == "up":
            cfg = load_config()
            up.run(cfg, dry_run=args.dry_run)
        elif args.command == "down":
            cfg = load_config()
            down.run(cfg, steps=args.steps)
        elif args.command == "status":
            cfg = load_config()
            status.run(cfg)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
