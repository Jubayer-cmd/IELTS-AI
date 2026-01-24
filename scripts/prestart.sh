#!/bin/bash
set -e

echo "Running pre-start checks..."

# Wait for database
cd backend
uv run python -m app.backend_pre_start

# Run migrations
uv run alembic upgrade head

# Seed initial data
uv run python -m app.initial_data

echo "Pre-start complete!"
