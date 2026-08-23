#!/usr/bin/env bash
set -euo pipefail

sudo apt update
sudo apt install -y python3-pip python3-venv python3-dev

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Setup complete. Run: source .venv/bin/activate && python src/main.py"
