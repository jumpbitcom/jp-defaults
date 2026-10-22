---
applyTo: "**/sqlite/**/*.sql"
description: "SQLite 3 schema, query, pragma and migration rules"
---

# SQLite Guidelines
https://sqlite.org

## Purpose
Rules for writing and reviewing SQLite SQL (schema, queries, migrations) and for configuring SQLite connections from application code. Target: the **latest SQLite 3.x** release (3.50+); if a feature needs a newer version than the one bundled with the project's runtime or driver, say so in a comment. Write SQLite SQL, not MariaDB or T-SQL.

Applies to `.sql` files under a `sqlite/` folder. In a repository that only uses SQLite, you can widen `applyTo` to `**/*.sql`.

## When to use SQLite
- Local development, tests, desktop and mobile apps, embedded devices, single-node services and read-heavy workloads.
- Not for many concurrent writers across processes or hosts; use MariaDB or a managed database there.

## General style
- Keywords in UPPER CASE, identifiers in `snake_case` lower case. One clause per line.
- End every statement with `;`. Comment intent with `--`.
- No `SELECT *` in application code; always list columns in `INSERT`.
- Use explicit `JOIN ... ON`, never comma joins; prefix columns with table aliases in multi-table queries.

## Naming
- Tables `snake_case`, singular or plural but consistent across the schema. Primary key `id` or `<table>_id`, consistent project-wide.
- Indexes `idx_<table>_<cols>`, unique indexes `uq_<table>_<cols>`, triggers `trg_<table>_<timing>_<event>`.

## Schema
- Create tables as `STRICT` so column types are enforced; use only `INTEGER`, `REAL`, `TEXT`, `BLOB` and `ANY`.
- Use `INTEGER PRIMARY KEY` for surrogate keys (alias of `rowid`); add `AUTOINCREMENT` only when ids must never be reused. Consider `WITHOUT ROWID` for tables with a non-integer or composite primary key.
- Declare `NOT NULL`, `UNIQUE`, `CHECK` and `FOREIGN KEY ... ON DELETE` constraints explicitly.
- Store dates as ISO 8601 `TEXT` in UTC (`'2026-10-22T08:15:00Z'`) or Unix epoch `INTEGER`, consistently per project. Store money as `INTEGER` minor units, never `REAL`.
- Store booleans as `INTEGER` with `CHECK (col IN (0, 1))`.
- Store JSON as `TEXT` with `CHECK (json_valid(col))`, or as JSONB `BLOB` (`jsonb()`) for heavy processing; index JSON paths through generated columns.
- Use generated columns (`GENERATED ALWAYS AS (...) STORED|VIRTUAL`) instead of duplicated data maintained by triggers.

## Queries
- Use bound parameters (`?` or `:name`) from application code; never build SQL with string interpolation.
- Use `INSERT ... ON CONFLICT DO UPDATE` (upsert) and `RETURNING` instead of select-then-write patterns.
- Use CTEs and window functions for readability; check query plans with `EXPLAIN QUERY PLAN` and add indexes for frequent filters and joins. Use partial indexes (`WHERE ...`) for sparse conditions.
- Use FTS5 for full-text search instead of `LIKE '%term%'`.

## Connections and pragmas
- Set on every connection: `PRAGMA foreign_keys = ON;` (off by default), `PRAGMA busy_timeout = 5000;`.
- Set once per database: `PRAGMA journal_mode = WAL;` for concurrent readers with one writer; `PRAGMA synchronous = NORMAL;` in WAL mode unless durability of the last transaction on power loss is required.
- Use one writer connection (or serialize writes) and short transactions; start write transactions with `BEGIN IMMEDIATE` to avoid deadlock-style `SQLITE_BUSY` errors.
- Run `PRAGMA optimize;` before closing long-lived connections.
- Don't put the database file on network file systems.

## Migrations
- Version the schema with the migration tool used by the project (Alembic, EF Core migrations, or numbered SQL files with `PRAGMA user_version`).
- For changes `ALTER TABLE` can't do, follow the SQLite 12-step procedure: create the new table, copy data, drop the old table, rename, recreate indexes and triggers, inside one transaction with `PRAGMA foreign_keys = OFF` and a `PRAGMA foreign_key_check` afterwards.

## Security and operations
- Never store secrets in plain text in the database; restrict file permissions on the database file.
- Back up with the online backup API or `VACUUM INTO 'backup.db'`, never by copying an open database file.
- Treat database files from untrusted sources as untrusted input; open them read-only and run `PRAGMA integrity_check` (or `quick_check`) first.
