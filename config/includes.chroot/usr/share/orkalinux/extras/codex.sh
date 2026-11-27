#!/bin/sh
set -e
curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_NON_INTERACTIVE=1 sh
echo
echo "Codex: open a new terminal and type  codex"
