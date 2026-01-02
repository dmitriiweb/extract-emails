# Debug Logging Rules

## Principles
- Add logs where they improve understanding of flow or failures; skip obvious/trivial steps.
- Do not modify behavior: add logs only, no refactors or control-flow changes.
- Keep log level at debug/trace unless the codebase dictates otherwise.
- Prefer few high-signal logs over verbose narration.

## Where to log
- Entry/exit of important functions, jobs, or request handlers.
- Around decision points: branching on feature flags, retries, fallbacks, or error paths.
- Before/after external calls (DB, APIs, queues, filesystem) with key identifiers and outcomes.
- When handling unexpected states or recoverable errors.
- Loops: log summaries (counts, keys) instead of every iteration unless debugging a specific item.

## What to log
- Action being taken and why (if not obvious), plus inputs that influence the path.
- Key identifiers: IDs, counts, types, feature flags; avoid PII/secrets.
- Outcomes: success/failure, status codes, elapsed time if easy to capture safely.
- Correlation IDs or request IDs when available to tie logs together.

## Avoid
- Logging every step or restating code that is already obvious.
- Adding expensive computations solely for logging.
- Reordering logic, altering return values, or changing error handling.
- Duplicating existing logs unless adding missing context.

## Safety and style
- Match existing logging conventions (logger name, structured fields, prefixes).
- Keep messages concise and consistent; prefer structured fields when supported.
- Ensure logs will not overwhelm hot paths; consider rate limiting if the codebase supports it.
