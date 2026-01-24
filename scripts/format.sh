#!/bin/bash
set -e

echo "Formatting code..."
cd backend
uv run ruff format .
uv run ruff check --fix .
