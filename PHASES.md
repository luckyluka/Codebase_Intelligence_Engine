# Codebase Intelligence Engine — Phases

This document defines the strict build order.  
**Do not skip phases. Do not expand scope inside phases.**

---

# PHASE 1 — Scanner (DONE)

Output:
- Flat list of files
- Metadata: path, size, modified_at, language

Goal:
- Deterministic filesystem traversal
- Zero AI involvement

---

# PHASE 2 — Structure Builder (ACTIVE)

## Objective
Convert raw files → structured code model.

This phase introduces the first **semantic layer**:
- functions
- imports
- file structure

NO AI YET (optional later extension).  
Must be deterministic.

---

## Core Output Schema (v0)

Each file becomes:

```json
{
  "path": "./scanner.py",
  "language": "python",
  "imports": [],
  "functions": []
}