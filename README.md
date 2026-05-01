# US Supply Chain Intelligence System (MVP)

Deterministic, evidence-first pipeline for compiling a dashboard dataset for newcleo's US partnership/supply-chain landscape.

## What this MVP includes

- Python package `supply_chain` with:
  - SQLModel data model for core entities
  - seed import from CSV/Excel
  - deterministic capability + relevance classification
  - connector stubs for official sources
  - dashboard JSON export
  - multi-sheet Excel export
- CLI commands via `supply-chain`
- `.env.example` with backend-only secrets
- basic tests for identity resolution, source grading, capability linkage, and export schema

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
```

Run pipeline:

```bash
supply-chain seed-import --input data/seed/vendors.csv
supply-chain enrich identity --all
supply-chain classify capabilities --all
supply-chain classify newcleo-relevance --all
supply-chain export dashboard-json --out public/data
supply-chain export excel --out exports/newcleo_us_supply_chain_enriched.xlsx
```

## Design constraints

- No subjective fields (priority/attractiveness/recommendations) are auto-generated.
- Every capability tag is tied to at least one `evidence_items` record.
- `unverified` claims are excluded from public dashboard export.
- API keys stay server-side only.
