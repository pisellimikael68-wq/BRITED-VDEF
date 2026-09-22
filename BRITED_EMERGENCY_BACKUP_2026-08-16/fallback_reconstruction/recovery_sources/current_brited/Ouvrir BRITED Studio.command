#!/bin/bash
set -u

BRITED_DIR="/Users/mikael_piselli/Documents/BRITED"
PYTHON_BIN="$BRITED_DIR/.venv/bin/python"

if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN="$BRITED_DIR/.venv-1/bin/python"
fi

if [ ! -x "$PYTHON_BIN" ]; then
  osascript -e 'display alert "BRITED Studio" message "L’environnement Python de BRITED est introuvable." as critical'
  exit 1
fi

if [ ! -f "$BRITED_DIR/studio_v2/app.py" ]; then
  osascript -e 'display alert "BRITED Studio" message "Le fichier principal studio_v2/app.py est introuvable." as critical'
  exit 1
fi

cd "$BRITED_DIR" || exit 1

# Évite de lancer deux serveurs sur le même port.
if /usr/sbin/lsof -nP -iTCP:8501 -sTCP:LISTEN >/dev/null 2>&1; then
  open "http://localhost:8501"
  exit 0
fi

LOG_FILE="$BRITED_DIR/.brited-studio.log"
nohup "$PYTHON_BIN" -m streamlit run "$BRITED_DIR/studio_v2/app.py" \
  --server.address 127.0.0.1 \
  --server.port 8501 \
  --server.headless true \
  >"$LOG_FILE" 2>&1 &

for attempt in {1..30}; do
  if /usr/bin/curl -fsS "http://127.0.0.1:8501/_stcore/health" >/dev/null 2>&1; then
    open "http://localhost:8501"
    exit 0
  fi
  sleep 1
done

osascript -e 'display alert "BRITED Studio" message "Le serveur n’a pas démarré. Consultez le fichier .brited-studio.log dans le dossier BRITED." as critical'
exit 1
