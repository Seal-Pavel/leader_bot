#!/bin/bash

set -e

echo "[INFO] Launching the uvicorn server."
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info

