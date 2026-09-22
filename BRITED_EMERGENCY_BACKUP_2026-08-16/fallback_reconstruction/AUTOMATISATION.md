# Automatisation quotidienne BRITED

La chaîne traite deux sujets par jour, chacun décliné nativement pour TikTok,
Instagram Reels et YouTube Shorts.

## Fonctionnement

1. À 10 h, le créneau 1 sélectionne le premier sujet du calendrier du jour.
2. À 17 h, le créneau 2 sélectionne le second sujet.
3. Un script propre mais construit avec une ancienne structure est refusé.
4. Les scripts natifs manquants sont générés et passent les contrôles BRITED.
5. La voix locale est produite beat par beat à partir de la référence validée.
6. Le rendu reprend le format social validé : texte progressif, question
   OUI/NON, page-réponse distincte, pictogrammes et clôture générique.
7. Un manifeste rassemble les vidéos, durées, alertes et empreintes SHA-256.
8. Le manifeste reste `awaiting_approval` et `publish_locked: true` jusqu'à la
   validation explicite de Mikael.

Les sorties se trouvent dans `production/AAAA-MM-JJ/slot-1` et `slot-2`.

## Sécurité de publication

Une vidéo modifiée après l'aperçu ne peut pas être approuvée : son empreinte ne
correspond plus au manifeste. La chaîne ne possède aucun chemin de publication
automatique tant que les comptes sociaux et leurs autorisations n'ont pas été
connectés. Cette absence est volontaire : aucune publication implicite.
