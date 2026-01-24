#!/bin/bash
set -e

# Generate TypeScript client from OpenAPI spec
echo "Generating frontend API client..."

# Start backend temporarily to get OpenAPI spec
cd backend
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
sleep 3

# Generate client
cd ../frontend
npm run generate-client

# Stop backend
kill $BACKEND_PID

echo "Client generated successfully!"
