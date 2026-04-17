#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/teammatch/backend"
FRONTEND_DIR="$ROOT_DIR/teammatch/frontend"

BACKEND_HOST="${BACKEND_HOST:-0.0.0.0}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_HOST="${FRONTEND_HOST:-0.0.0.0}"
FRONTEND_PORT="${FRONTEND_PORT:-3000}"

if ! command -v npm >/dev/null 2>&1; then
  echo "Error: npm is required but not found in PATH."
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: python3/python is required but not found in PATH."
  exit 1
fi

if ! "$PYTHON_BIN" -m uvicorn --version >/dev/null 2>&1; then
  echo "Error: uvicorn is not available in the current Python environment."
  echo "Install backend deps first (example):"
  echo "  cd $BACKEND_DIR && $PYTHON_BIN -m pip install -r requirements.txt"
  exit 1
fi

if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
  echo "Warning: frontend node_modules directory not found."
  echo "Run: cd $FRONTEND_DIR && npm install"
fi

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  echo
  echo "Stopping dev processes..."

  if [[ -n "$FRONTEND_PID" ]] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
    kill "$FRONTEND_PID" 2>/dev/null || true
  fi

  if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi

  wait 2>/dev/null || true
}

trap cleanup INT TERM EXIT

echo "Starting TeamMatch local dev/debug stack (no Docker)..."
echo "Backend:  http://localhost:$BACKEND_PORT"
echo "Frontend: http://localhost:$FRONTEND_PORT"

(
  cd "$BACKEND_DIR"
  "$PYTHON_BIN" -m uvicorn app.main:app \
    --reload \
    --host "$BACKEND_HOST" \
    --port "$BACKEND_PORT" \
    --log-level debug
) &
BACKEND_PID=$!

(
  cd "$FRONTEND_DIR"
  npm run dev -- --hostname "$FRONTEND_HOST" --port "$FRONTEND_PORT"
) &
FRONTEND_PID=$!

wait -n "$BACKEND_PID" "$FRONTEND_PID"
