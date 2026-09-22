# BRITED Studio — version finale restaurée

Cette installation fonctionne exclusivement depuis son dossier local, hors
iCloud et hors Google Drive. Les réglages finaux ont été reconstruits depuis
l'export ChatGPT et les journaux Codex, sans utiliser de contenu inventé comme
source juridique ou fiscale.

- Serveur : http://127.0.0.1:8766
- Deux créneaux quotidiens : 10 h et 17 h
- Plateformes : TikTok, Instagram Reels, YouTube Shorts
- Publication : toujours verrouillée jusqu'à validation humaine
- Corpus : 75 fiches complètes retrouvées sur 84 sujets catalogués
- Sujets incomplets : 9, bloqués automatiquement jusqu'à restauration ou
  nouvelle certification factuelle
- Référence TikTok : `Pilote_tiktok_V33_fluidite_totale.mp4`
- Calendrier : 180 jours, 2 sujets par jour, 1 script/vidéo YouTube source par créneau, diffusé à l'identique sur 4 plateformes
- Production : file persistante avec reprise, erreurs isolées par plateforme
- Contrôles vidéo : mots rendus, images finales, 1080 × 1920, audio, durée et synchronisation
- Automatisation macOS : service `com.brited.studio`, actif à l'ouverture de session
- Notifications : créneau prêt à vérifier ou bloqué
- Export : `production/AAAA-MM-JJ/slot-N/plateforme`

## Ouverture

Double-cliquez sur `Ouvrir BRITED Studio.command`. Gardez la fenêtre Terminal
ouverte pendant l'utilisation. Le navigateur s'ouvre automatiquement.

## Sauvegarde

Double-cliquez sur `sauvegarder.command`. Une copie datée est créée dans
`/Users/mikael_piselli/BRITED_LOCAL_BACKUPS`, sans le fichier secret `.env`.
