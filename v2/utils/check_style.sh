#!/bin/bash

# --------------------------------------------
# CivicLens: check code with Black and Ruff
# --------------------------------------------

set -e

echo "=== Running Black check ==="
black --check ./ || {
    echo "Black formatting issues found"
    exit 1
}

echo "=== Running Ruff check ==="
ruff check ./ || {
    echo "Ruff lint issues found"
    exit 1
}

echo "All style checks passed ✅"
exit 0


if [ $? -ne 0 ]; then
    echo "Ruff lint issues found"
    exit 1
fi

echo "All style checks passed"
exit 0
