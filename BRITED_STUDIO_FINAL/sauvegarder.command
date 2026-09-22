#!/bin/bash
set -e
SOURCE="$(cd "$(dirname "$0")" && pwd)"
DESTINATION="/Users/mikael_piselli/BRITED_LOCAL_BACKUPS/$(date +%Y-%m-%d_%H-%M-%S)"
mkdir -p "$DESTINATION"
rsync -a --exclude '.env' --exclude '__pycache__' --exclude '*.pyc' "$SOURCE/" "$DESTINATION/"
echo "Sauvegarde locale créée : $DESTINATION"
read -r -p "Appuyez sur Entrée pour fermer…"
