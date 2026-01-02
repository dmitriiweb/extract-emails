# AGENTS.md — Agent instructions for this repository

## Goals
- Primary goal: (e.g., ship correct changes with tests passing)
- Secondary goals: (e.g., minimal diffs, keep public APIs stable)

## Setup & daily commands (run these)
- Install deps: `...`
- Start dev: `...`
- Lint: `...`
- Format: `...`
- Typecheck: `...`
- Test (all): `...`
- Test (single): `...`  <!-- include an example like pytest path::test_name -->
- Build: `...`

## Repo map (where to look / write)
- `src/` — ...
- `tests/` — ...
- `docs/` — ...
- `scripts/` — ...
- Generated / do-not-edit: `...`

## Architecture snapshot
- Component A → Component B → Database/Queue/Cache
- Key entrypoints: `...`
- Key configs: `...`

## Dev environment
- Required versions: (language/runtime/tooling)
- Required services: (db, redis, kafka, etc.)
- Env vars: (list + where to get them)
- Migrations/seed: `...`

## Workflow rules
- Branching: `...`
- PR expectations: (tests, lint, docs updates)
- Release/versioning: `...`

## Code style & patterns
- Formatting: (prettier/ruff/black/etc.)
- Conventions: (naming, imports, layering)
- Error handling: (how to surface errors, retries, logging)
- Example (good):
  ```lang
  ...

## Example (filled)
```markdown
# AGENTS.md — Agent instructions for this repository

## Goals
- Primary goal: ship correct changes with tests passing
- Secondary goals: minimal diffs, keep public APIs stable

## Setup & daily commands (run these)
- Install deps: `uv sync`
- Start dev: `uv run python -m app`
- Lint: `make lint`
- Format: `make format`
- Typecheck: `make typecheck`
- Test (all): `pytest`
- Test (single): `pytest tests/test_api.py::test_list_items`
- Build: `make build`

## Repo map (where to look / write)
- `src/` — application source
- `tests/` — pytest tests
- `docs/` — project documentation
- `scripts/` — developer scripts
- Generated / do-not-edit: `dist/`, `build/`, `node_modules/`

## Architecture snapshot
- API → service layer → Postgres
- Key entrypoints: `src/app.py`, `src/cli.py`
- Key configs: `pyproject.toml`, `config/settings.toml`

## Dev environment
- Required versions: Python 3.12, uv 0.4
- Required services: Postgres 15
- Env vars: `DATABASE_URL` (from `.env`), `SENTRY_DSN` (1Password)
- Migrations/seed: `uv run alembic upgrade head`

## Workflow rules
- Branching: feature branches from `main`
- PR expectations: lint + tests required, update docs when behavior changes
- Release/versioning: semantic versioning, tag via CI

## Code style & patterns
- Formatting: ruff format
- Conventions: snake_case modules, keep domain logic in `src/domain`
- Error handling: raise `AppError`, log via `structlog`
- Example (good):
  ```python
  def list_items(repo: ItemRepo) -> list[Item]:
      return repo.list()
  ```
```
