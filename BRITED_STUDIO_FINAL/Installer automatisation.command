#!/bin/bash
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
TARGET="$HOME/Library/LaunchAgents/com.brited.studio.plist"
mkdir -p "$HOME/Library/LaunchAgents"
cp "$HERE/automation/com.brited.studio.plist" "$TARGET"
launchctl bootout "gui/$(id -u)/com.brited.studio" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$TARGET"
launchctl enable "gui/$(id -u)/com.brited.studio"
open http://127.0.0.1:8766
echo "BRITED Studio démarrera automatiquement avec votre session Mac."
