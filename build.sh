#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python seed_render.py
