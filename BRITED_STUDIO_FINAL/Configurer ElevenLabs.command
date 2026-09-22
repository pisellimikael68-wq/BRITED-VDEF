#!/bin/bash
set -euo pipefail

ROOT="/Users/mikael_piselli/BRITED_STUDIO_FINAL"
CONFIG="$ROOT/config/voice-provider.json"

printf "Identifiant de voix ElevenLabs : "
IFS= read -r VOICE_ID
if [ -z "$VOICE_ID" ]; then
  echo "Identifiant vide : configuration annulée."
  exit 1
fi
printf "Clé API ElevenLabs (saisie masquée) : "
IFS= read -rs API_KEY
echo
if [ -z "$API_KEY" ]; then
  echo "Clé vide : configuration annulée."
  exit 1
fi

security add-generic-password -U -a "$USER" -s BRITED_ELEVENLABS_API_KEY -w "$API_KEY" >/dev/null
"$ROOT/.venv/bin/python" - "$CONFIG" "$VOICE_ID" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
data["voice_id"] = sys.argv[2].strip()
data["active_provider"] = "local"
data["preview_provider"] = "elevenlabs"
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
unset API_KEY
echo
echo "ElevenLabs est configuré pour les aperçus."
echo "La production reste sur la voix locale jusqu'à votre validation."
read -r -p "Appuyez sur Entrée pour fermer…"
