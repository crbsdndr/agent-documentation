---
name: database-schema
description: "MUST view this before creating, altering, or reviewing database tables, columns, relations, RLS policies, or migrations. Contains schema source of truth and Supabase best practices."
---
# Database Schema Skill

## Master Rules

- Normalize to 5NF by default — denormalize only with proven performance need and document the reason
- Use snake_case everywhere — plural nouns for tables, `_id` suffix for foreign keys, `is_`/`has_`/`can_` for booleans, `_at` for timestamps
- Use `uuid` for primary keys, `timestamptz` for timestamps, `text` over `varchar`, `jsonb` only for truly dynamic data
- Define explicit foreign keys with appropriate `ON DELETE` behavior on every relation
- Index foreign keys and columns used in WHERE, ORDER BY, or JOIN — do not over-index
- Enable RLS on every table with user data — default deny, grant access explicitly
- Every schema change must go through a migration — one concern per migration, reversible when possible
- When adding a field to the schema, always include: column name, data type, constraints, and an example value

---

## Dynamic Rules

- Update this file whenever the schema changes — this file is the source of truth
- Add new tables and columns to the Schema section before or immediately after migration
- Remove dropped tables and columns from the Schema section
- Do not let the Schema section drift from the actual database state

---

## Schema

Write in here