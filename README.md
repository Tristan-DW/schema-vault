<div align="center">

<img src="https://skillicons.dev/icons?i=nodejs,sqlite,postgres,bash" />

<br/>

![GitHub last commit](https://img.shields.io/github/last-commit/Tristan-DW/schema-vault?style=for-the-badge&color=6e40c9)
![GitHub stars](https://img.shields.io/github/stars/Tristan-DW/schema-vault?style=for-the-badge&color=f0883e)
![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-238636?style=for-the-badge)

# schema-vault

> **Database schema management and migration CLI - version-controlled, diff-aware, multi-driver.**

</div>

---

## Overview

**schema-vault** is a lightweight CLI tool for managing database schemas across environments. Define your schema in SQL files, track applied migrations in a lock table, diff against live databases, and roll back safely - all from the terminal.

---

## Features

| Feature | Description |
|---|---|
| **Multi-driver** | Supports PostgreSQL, MySQL, and SQLite |
| **Migration tracking** | Applied migrations stored in a `_schema_vault` lock table |
| **Diff engine** | Compare migration state across environments |
| **Rollback** | Reverse migrations with down scripts |
| **Dry run** | Preview SQL before applying |
| **Status command** | Shows pending vs applied migrations at a glance |
| **Init** | Scaffold a new project in seconds |

---

## Quick Start

```bash
npm install -g schema-vault

# Initialize a new project
sv init my-project
cd my-project

# Create your first migration
sv create add_users_table

# Apply pending migrations
sv up

# Check migration status
sv status

# Roll back last migration
sv down
```

---

## Commands

| Command | Description |
|---|---|
| `sv init [name]` | Scaffold a new schema-vault project |
| `sv create <name>` | Generate a new timestamped migration file |
| `sv up [--dry-run]` | Apply all pending migrations |
| `sv down [--steps N]` | Roll back N migrations (default: 1) |
| `sv status` | List applied and pending migrations |
| `sv diff` | Show SQL diff between local and remote state |
| `sv reset` | Drop and re-apply all migrations (dev only) |

---

## Migration File Format

```sql
-- migrations/20240315_001_add_users_table.sql
-- up
CREATE TABLE users (
  id         SERIAL PRIMARY KEY,
  email      VARCHAR(255) UNIQUE NOT NULL,
  name       VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- down
DROP TABLE IF EXISTS users;
```

---

## Configuration

```json
{
  "driver": "postgres",
  "connection": "postgresql://user:pass@localhost:5432/mydb",
  "migrationsDir": "./migrations",
  "lockTable": "_schema_vault"
}
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
