# Spécification haute fidélité — Visuel B (plein cadre structuré)

Canvas de référence : **1080 × 1920 px**, sans marque visible. Contenu, chiffres et ordre narratif identiques au script certifié « Changer de régime matrimonial en cours de mariage ». Cette fiche sert de référence d'intégration pour le moteur vidéo local.

## Jetons partagés (toutes pages)

| Élément | Valeur |
|---|---|
| Fond | `#FFFEFA` (ivoire) |
| Encre (texte principal) | `#201C16` |
| Ocre (accent) | `#D99A2B` |
| Ocre foncé (texte sur accent clair) | `#A9711A` |
| Gris atténué (labels secondaires) | `#6B6255` |
| Séparateur | `rgba(32,28,22,0.12)`, 1px |
| Module inactif (bordure) | `#D99A2B` |
| Module actif (fond + bordure) | fond `#F3E0BE`, bordure `#A9711A` |
| Marges latérales de sécurité | 72 px (zone de contenu utile : 936 px) |
| Police titres | Archivo Black (fallback : Helvetica Neue Bold condensé) |
| Police labels / UI | Inter, graisses 700–800 |

## Composants réutilisables

- **Cartouche titre thématique** : label « RÉGIME MATRIMONIAL », Inter ExtraBold 800, 30px, lettrage +0.12em, majuscules, couleur ocre foncé. Position : x=72, y=64. Trait ocre dessous : largeur 96px, hauteur 4px, radius 999px, marge haut 14px.
- **Séparateur horizontal** : ligne 1px pleine largeur utile (936px), centrée x=540, position fixe y=1540 (sépare le bloc de texte du bloc pictogrammes).
- **Module pictogramme** : carré 168×168px, radius 20px. Inactif : bordure 2px ocre, fond transparent, icône 72×72 centrée, trait ocre. Actif (mise en avant du concept clé de la page) : fond `#F3E0BE`, bordure 2px `#A9711A`, icône `#A9711A`. Gap entre modules : 28px. Connecteur (trait horizontal 16×2px, `rgba(32,28,22,0.25)`) uniquement entre 2 modules adjacents sans emphase.
- **Ligne de modules** : centrée horizontalement, y=1620 (entre séparateur et progression).
- **Barre de progression** : y=1840, hauteur 10px, 7 segments égaux, largeur segment 122px, gap 14px, radius 999px. Actif : `#D99A2B`. Inactif : `rgba(32,28,22,0.1)`. Toujours en bas uniquement, jamais en haut.
- **Titre principal** : centré, largeur max 936px, lettrage -0.01em, interligne 1.18, majuscules, `#201C16`. Taille adaptative : ≤3 lignes → 84px ; 4 lignes → 72px ; 5–6 lignes → 60px. Centré verticalement entre le cartouche (fin ~170px) et le séparateur (1540px).
- **Label secondaire** (ex. « À vous de jouer ») : Inter ExtraBold 800, 26px, lettrage +0.1em, majuscules, `#6B6255`, marge basse 32px avant le titre.
- **Boutons OUI / NON** : hauteur 96px, padding horizontal 64px, radius 16px, Inter ExtraBold 800, 34px, majuscules. OUI : fond `#D99A2B`, texte blanc. NON : fond transparent, bordure 3px `#201C16`, texte `#201C16`. Gap 20px. OUI et NON ne sont ni lus ni répétés dans la question.
- **Pastille NON (écran réponse)** : fond `#201C16`, texte blanc, hauteur 84px, padding horizontal 56px, radius 16px, Inter ExtraBold 800, 32px, majuscules, marge basse 40px avant le titre.
- **Bouton CTA rendez-vous** : fond `#F3E0BE`, bordure 3px `#D99A2B`, texte `#A9711A`, hauteur 112px, padding horizontal 72px, radius 20px, Inter ExtraBold 800, 38px, majuscules.
- **Sous-texte CTA** : Inter ExtraBold 800, 28px, lettrage +0.06em, majuscules, `#A9711A`, marge haut 28px.

## Écrans (contenu verbatim du script certifié)

1. **Accroche** — Titre : « Changer de régime est possible. Mais le notaire suffit-il ? » (4 lignes → 72px). Modules : `users` + `heart-handshake` (connecteur, aucun n'est actif). Progression 1/7.
2. **Question** — Label « À vous de jouer ». Titre : « Selon vous, l'acte notarié suffit-il ? » (60px). Boutons OUI / NON. Pas de pictogramme sur cet écran. Progression 2/7.
3. **Réponse** — Pastille NON. Titre : « L'acte est indispensable, mais d'autres étapes s'ajoutent. » (60px). Pas de pictogramme. Progression 3/7.
4. **Nuance / précision** — Titre : « En cas d'opposition, le tribunal homologue l'acte. Pour un mineur, le notaire peut saisir le juge si ses intérêts semblent menacés. » (60px, 5 lignes). Modules : `scale` (inactif), `shield-check` (actif — mis en avant), `users` (inactif). Progression 4/7.
5. **Exemple** — Titre : « Exemple : un entrepreneur choisit la séparation de biens pour mieux isoler son conjoint du risque professionnel. » (60px). Modules : `landmark` (inactif), `shield-check` (actif). Progression 5/7.
6. **Nuance fiscale** — Titre : « Attention : ce choix peut avoir des conséquences successorales et fiscales. Mesurez ses effets avant de signer. » (60px). Modules : `file-text` (inactif), `users` (actif), `percent` (inactif). Progression 6/7.
7. **CTA rendez-vous** — Titre : « Vous souhaitez faire le point sur votre situation ? » (72px). Bouton CTA : « Prenez rendez-vous ». Sous-texte : « via le lien dans ma bio ». Module unique : `calendar` (centré, sans cadre carré — icône seule, taille 96×96). Progression 7/7 (pleine).

## Pictogrammes exportés

Dossier `pictogrammes-export/` — SVG Lucide bruts (`stroke="currentColor"`, viewBox 24×24), prêts à être recolorés et redimensionnés (168px module / 72px icône, ou 24px natif × facteur d'échelle) par le moteur vidéo :
`01-hook-users.svg`, `01-hook-heart-handshake.svg`, `04-precision-scale.svg`, `04-precision-shield-check.svg`, `04-precision-users.svg`, `05-exemple-landmark.svg`, `05-exemple-shield-check.svg`, `06-nuance-file-text.svg`, `06-nuance-users.svg`, `06-nuance-percent.svg`, `07-cta-calendar.svg`.
