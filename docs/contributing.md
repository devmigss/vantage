# Contributing Guidelines

To keep the `Vantage` repository clean, reliable, and readable, please follow these branching, coding, testing, and commit conventions.

---

## Commit Message Convention

We follow the **Conventional Commits** format:

`<type>: <description>`

### Types
- `feat:` A new feature for the user or API (e.g., `feat: add city and ASN fields to network fetch`)
- `fix:` A bug fix (e.g., `fix: handle request timeout in network API`)
- `chore:` Maintenance tasks, dependency updates, or setup (e.g., `chore: add requirements.txt`)
- `docs:` Documentation changes only (e.g., `docs: update CONTRIBUTING.md`)
- `refactor:` Code changes that neither fix a bug nor add a feature

### Rules
- Use lowercase for the type and description.
- Use the imperative mood in the description ("add" not "added" or "adds").
- Do not end the commit message with a period.