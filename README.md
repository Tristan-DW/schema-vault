<div align="center">

<img src="https://skillicons.dev/icons?i=python,postgres,mysql,sqlite,bash" />

<br/>

![GitHub last commit](https://img.shields.io/github/last-commit/Tristan-DW/schema-vault?style=for-the-badge&color=6e40c9)
![GitHub stars](https://img.shields.io/github/stars/Tristan-DW/schema-vault?style=for-the-badge&color=f0883e)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-238636?style=for-the-badge)

# schema-vault

> **Database schema management and migration CLI - Python, version-controlled, diff-aware, multi-driver.**

</div>

---

## Overview

**schema-vault** is a Python CLI tool for managing database schemas across environments. Define your schema in `.sql` files, track applied migrations in a lock table, diff against live databases, and roll back safely - all from the terminal. Supports PostgreSQL, MySQL, and SQLite with a consistent interface.

---

## Features

| Feature | Description |
|---|---|
| **Multi-driver** | PostgreSQL, MySQL, and SQLite with a unified API |
| **Migration tracking** | Applied migrations stored in a `_schema_vault` lock table |
| **Rollback** | Reverse migrations with `-- down` scripts |
| **Dry run** | Preview SQL before applying with `--dry-run` |
| **Status command** | Pending vs applied at a glance |
| **Init** | Scaffold a new project with `sv init` |
| **Python native** | No Node.js required - pure Python, installable via pip |

---

## Quick Start

```bash
pip install schema-vault

# Initialize a project
sv init my-project
cd my-project

# Create a migration
sv create add_users_table

# Apply pending migrations
sv up

# Check status
sv status

# Roll back last migration
sv down
```

---

## Commands

| Command | Description |
|---|---|
| `sv init [name]` | Scaffold a new project |
| `sv create <name>` | Generate a timestamped migration file |
| `sv up [--dry-run]` | Apply pending migrations |
| `sv down [--steps N]` | Roll back N migrations (default: 1) |
| `sv status` | Show applied and pending migrations |
| `sv reset` | Drop and re-apply all (dev only) |

---

## Migration Format

```sql
-- migrations/20240315_001_add_users_table.sql

-- up
CREATE TABLE users (
  id         SERIAL PRIMARY KEY,
  email      VARCHAR(255) UNIQUE NOT NULL,
  name       VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- down
DROP TABLE IF EXISTS users;
```

---

## Configuration

```toml
# schema-vault.toml
driver = "postgres"
connection = "postgresql://user:pass@localhost:5432/mydb"
migrations_dir = "./migrations"
lock_table = "_schema_vault"
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

<div align="center">

<sub>Architected by <a href="https://github.com/Tristan-DW">Tristan</a> - Head Architect</sub>

</div>
