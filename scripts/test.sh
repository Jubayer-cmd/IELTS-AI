#!/bin/bash
set -e

echo "Running backend tests..."
cd backend
uv run pytest "${@}"
