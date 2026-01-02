# Format and Lint Rules

## Commands
- Format: `make format`
- Linters and mypy: `make lint`

## Order of operations
- Always run `make format` before linting to apply formatting changes.  
- Run `make lint`.  
- If linters fail, fix those issues first and rerun `make lint` to confirm the lint errors are resolved.  
- After lint issues are clear, fix any mypy errors surfaced by `make lint`, then rerun `make lint` to verify.  
- Continue iterating until `make lint` completes without errors.  

## Handling mypy dependencies
- When mypy reports missing libraries or type stubs, add the required package with `uv add --dev <package>` so it lands in the dev dependencies of `pyproject.toml`.  
- Do **not** use mypy's "install missing libraries" command or flags.  

## Reporting
- Note which commands were run and their outcomes.  
- Call out any remaining issues or blockers after the final `make lint` run.  
