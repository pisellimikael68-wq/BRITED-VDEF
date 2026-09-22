#!/bin/bash
set -u
URL="http://127.0.0.1:8766/"
LABEL="gui/$(id -u)/com.brited.studio"

# Le service est maintenu par macOS : fermer ce terminal ne coupe plus le site.
launchctl kickstart "$LABEL" >/dev/null 2>&1 || true
for _ in {1..30}; do
  if curl -fsS --max-time 1 "${URL}api/health" >/dev/null 2>&1; then
    open "$URL"
    exit 0
  fi
  sleep 0.2
done

echo "BRITED Studio n'a pas démarré. Relancez ce raccourci dans quelques secondes."
read -r -p "Appuyez sur Entrée pour fermer."
exit 1
