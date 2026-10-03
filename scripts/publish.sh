#!/usr/bin/env bash
# Publica o .vsix gerado pelo semantic-release nas lojas cujos tokens existirem.
set -euo pipefail

VSIX=$(ls ./*.vsix | head -n 1)

if [ -n "${VSCE_PAT:-}" ]; then
  npx vsce publish --packagePath "$VSIX" -p "$VSCE_PAT"
else
  echo "VSCE_PAT ausente: pulando VS Code Marketplace"
fi

if [ -n "${OVSX_PAT:-}" ]; then
  npx ovsx publish "$VSIX" -p "$OVSX_PAT"
else
  echo "OVSX_PAT ausente: pulando Open VSX"
fi
