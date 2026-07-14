---
name: storage-path
description: "MUST view this before creating, reading, or managing Supabase Storage buckets, paths, or policies. Contains storage structure source of truth and best practices."
---
# Storage Path Skill

## Master Rules

- Name buckets in kebab-case with clear purpose (profile-photos, invoices, attachments)
- Use unique filenames to prevent overwrites — prefix with timestamp or uuid
- Set buckets as private by default — only make public when files genuinely need unauthenticated access
- Validate file type and size before upload — never trust client-side validation alone
- Define allowed MIME types per bucket — reject anything outside the whitelist
- When adding a bucket or path to the Storage section, always include: bucket name, visibility, allowed MIME types, max file size, and path pattern

---

## Dynamic Rules

- Update this file whenever storage structure changes — this file is the source of truth
- Add new buckets and path patterns to the Storage section before or immediately after implementation
- Remove deprecated buckets and paths from the Storage section
- Do not let the Storage section drift from the actual storage configuration

---

## Storage

Write in here