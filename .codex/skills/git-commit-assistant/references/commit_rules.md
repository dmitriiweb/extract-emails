# Git Commit Rules

## Conventional format
- Use `<type>(optional-scope): <summary>`
- Allowed types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `build`, `ci`, `perf`, `style`
- Scope is optional; keep it short (e.g., `api`, `auth`, `deps`)

## Summary line
- 50–72 characters, imperative mood, no trailing period
- Describe the what/why; avoid implementation detail

## Body (when needed)
- Explain why the change was needed and key decisions
- Note trade-offs or limitations
- Wrap lines around 72 characters

## Footers
- Use for breaking changes, issue references, migrations
- Examples:
  - `BREAKING CHANGE: rename UserModel to AccountModel`
  - `Closes #142`

## Quality gate
- Commit should contain related changes only; no kitchen-sink diffs
- Do not mix formatting-only changes with functional work
- Message must match the actual intent of the diff
- Avoid noisy summaries like `update`, `changes`, `fix stuff`, `wip`

## Output pattern
```
<type>(scope): <summary>

<body>

<footers>
```
Only include body/footers when they add value.

## Commit workflow for the agent
1) Inspect the diff or description and pick the correct `<type>`/scope.  
2) Draft the message (summary + optional body/footers) using the pattern above.  
3) Present the message in a fenced code block and ask for approval to commit.  
4) On approval, ensure the staged changes match the message, then run  
   `git status` (if helpful) and `git commit -m "<message>"` (or `git commit`  
   with `-m` plus body as needed). Do not commit unrelated or unstaged work.  
5) If the user declines, revise the message or exit without committing.
