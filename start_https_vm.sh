#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PORT="${HTTPS_PORT:-5000}"
ALT_PORT="${HTTPS_ALT_PORT:-5443}"
VM_IP="$(hostname -I 2>/dev/null | tr ' ' '\n' | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$' | head -n 1 || true)"
if [[ -z "$VM_IP" ]]; then
  VM_IP="127.0.0.1"
fi

echo "[1/4] Activating virtual environment"
source /home/train1234/.venv/bin/activate

echo "[2/4] Generating TLS certificate"
./setup_https_local.sh >/dev/null

echo "[3/4] Stopping old HTTPS server on ports ${PORT} and ${ALT_PORT} (if any)"
if command -v fuser >/dev/null 2>&1; then
  fuser -k "${PORT}/tcp" >/dev/null 2>&1 || true
  if [[ "${ALT_PORT}" != "${PORT}" ]]; then
    fuser -k "${ALT_PORT}/tcp" >/dev/null 2>&1 || true
  fi
fi

sleep 1

echo "[4/4] Starting HTTPS server"
HTTPS_PORT="${PORT}" nohup python run_ssl.py >/tmp/train1234_https.log 2>&1 &
PID=$!

ALT_PID=""
if [[ "${ALT_PORT}" != "${PORT}" ]]; then
  HTTPS_PORT="${ALT_PORT}" nohup python run_ssl.py >/tmp/train1234_https_${ALT_PORT}.log 2>&1 &
  ALT_PID=$!
fi

for _ in $(seq 1 20); do
  if curl -k -fsS "https://127.0.0.1:${PORT}/database" >/dev/null 2>&1; then
    echo
    echo "HTTPS is running."
    echo "Inside VM:  https://127.0.0.1:${PORT}"
    echo "Inside VM:  https://${VM_IP}:${PORT}"
    echo "Host Edge (with port forwarding): https://127.0.0.1:${PORT}"
    if [[ "${ALT_PORT}" != "${PORT}" ]] && curl -k -fsS "https://127.0.0.1:${ALT_PORT}/database" >/dev/null 2>&1; then
      echo "Inside VM:  https://127.0.0.1:${ALT_PORT}"
      echo "Inside VM:  https://${VM_IP}:${ALT_PORT}"
      echo "Host Edge alt (with port forwarding): https://127.0.0.1:${ALT_PORT}"
    fi
    echo "Log file: /tmp/train1234_https.log"
    if [[ -n "${ALT_PID}" ]]; then
      echo "Alt log file: /tmp/train1234_https_${ALT_PORT}.log"
    fi
    exit 0
  fi
  sleep 1
done

echo "Server process started with PID ${PID}, but health check failed."
if [[ -n "${ALT_PID}" ]]; then
  echo "Second server PID: ${ALT_PID}"
fi
echo "See logs: /tmp/train1234_https.log"
exit 1
