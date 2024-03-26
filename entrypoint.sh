#!/bin/bash

set -e

echo "[INFO] Launching the uvicorn server."
uvicorn main:app --reload --log-level info # dev host localhost and port 8000
#uvicorn main:app --host 0.0.0.0 --port 8000

