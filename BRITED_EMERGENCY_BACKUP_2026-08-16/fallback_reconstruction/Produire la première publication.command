#!/bin/bash
set -e
cd "/Users/mikael_piselli/Documents/BRITED"
exec ".venv/bin/python" -m leveria.daily --root "$PWD" --slot 1
