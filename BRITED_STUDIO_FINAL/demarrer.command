#!/bin/bash
cd "$(dirname "$0")" || exit 1
export BRITED_ROOT="$PWD"
python3 -m leveria.server
