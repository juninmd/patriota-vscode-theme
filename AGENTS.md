# AGENTS.md

## Overview
This file serves as a living memory and guide for AI agents (like Jules) working on the **Patriota Theme** repository. It outlines the project structure, development guidelines, and future roadmap.

## Project Structure
- `themes/patriota-color-theme.json`: The core theme definition file.
- `scripts/validate_theme.py`: Validation script for the theme JSON, including accessibility checks.
- `generate_preview.py`: Python script to generate an HTML preview and screenshot it using Playwright.
- `.github/workflows/`: CI/CD pipelines for testing and preview generation.

## Development Guidelines
- **Theme Updates:** Always run `python scripts/validate_theme.py` after modifying the theme.
- **Preview:** Run `python generate_preview.py` to visually verify changes before pushing.
- **Commits:** Use semantic commit messages (e.g., `feat: update syntax colors`, `fix: correct background hex`).
- **Tests:** Run `pytest tests/` to verify validation logic.

## Future Roadmap
The following tasks are high-priority improvements identified during the Antigravity Audit:

1.  **Automated Publishing (DevOps):**
    - Implement Semantic Release to automatically version and tag the repository.
    - Add a workflow to publish the extension to the VS Code Marketplace and Open VSX Registry upon release.

2.  **Expanded Preview (Docs/Tooling):**
    - Improve `generate_preview.py` to showcase more syntax examples (e.g., Markdown, CSS, HTML, TSX) to give a better overview of the theme's coverage.

## Learnings
- **2025-01-26:** Implemented strict Hex code validation in CI. This prevents invalid color codes from breaking the VS Code parser.
- **2025-02-18:** Added automated contrast ratio checks (WCAG AA) to `validate_theme.py`. Identified low contrast issues in `Tags` (#009c3b on #002776) and `Invalid` tokens.
- **2025-02-18:** Resolved low contrast issues by replacing `#009c3b` with `#3bdc75` (Brighter Green) in foregrounds to meet WCAG AA standards. Added `markup.inline.raw` styling.
