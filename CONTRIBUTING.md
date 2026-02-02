# Contributing to Patriota Theme

Thank you for your interest in contributing to the **Patriota** theme! We welcome contributions from everyone.

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally.
3.  **Install dependencies**:
    We recommend using [uv](https://github.com/astral-sh/uv) for dependency management.
    ```bash
    # Install dependencies
    uv pip install playwright pytest

    # Install Playwright browsers
    playwright install chromium
    ```

## Making Changes

1.  Modify `themes/patriota-color-theme.json`.
2.  **Validate your changes**:
    ```bash
    # Run unit tests
    python -m pytest tests/

    # Run theme validation
    python scripts/validate_theme.py
    ```
3.  **Generate a preview** to see how it looks:
    ```bash
    python generate_preview.py
    ```
    Open `preview.html` or check `theme_preview.png`.

## Submitting a Pull Request

1.  Push your changes to your fork.
2.  Open a Pull Request against the `main` branch.
3.  Ensure the CI checks pass.
4.  Provide a clear description of your changes and why they are needed.

## Code of Conduct

Please be respectful and kind to other contributors.
