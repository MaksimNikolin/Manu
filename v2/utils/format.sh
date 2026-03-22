#!/bin/bash

# ---------------------------------------------
# CivicLens: auto format with Black and Ruff
# ---------------------------------------------

set -e

echo "=== Formatting Python code with Black ==="
black ./

echo "=== Fixing lint issues with Ruff ==="
ruff check ./ --fix || true

BLACK_COUNT=$(black . --diff | grep "reformatted" | wc -l)
RUFF_COUNT=$(ruff check ./ --quiet | wc -l)

echo "Formatting complete!"
echo "Black reformatted files: $BLACK_COUNT"
echo "Ruff remaining issues: $RUFF_COUNT"