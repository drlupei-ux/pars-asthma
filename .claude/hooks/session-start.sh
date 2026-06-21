#!/bin/bash
set -euo pipefail

# Only run in remote (cloud) sessions
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Install Python dependencies
if [ -f "$CLAUDE_PROJECT_DIR/requirements.txt" ]; then
  pip install -r "$CLAUDE_PROJECT_DIR/requirements.txt" -q
fi

# Install superpowers plugin (idempotent)
if ! claude plugin list 2>/dev/null | grep -q "superpowers"; then
  claude plugin marketplace add obra/superpowers-marketplace --silent 2>/dev/null || true
  claude plugin install superpowers@superpowers-marketplace 2>/dev/null || true
fi

# Add context7 MCP server via npx (idempotent)
if ! claude mcp list 2>/dev/null | grep -q "context7"; then
  claude mcp add context7 -s user -- npx -y @upstash/context7-mcp@latest 2>/dev/null || true
fi
