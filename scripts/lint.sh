#!/bin/bash
set -e

echo "Running linters..."
cd backend
uv run ruff check .
uv run ruff format --check .
