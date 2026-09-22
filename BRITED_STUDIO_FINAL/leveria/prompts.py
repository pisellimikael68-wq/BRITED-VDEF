from __future__ import annotations

from .charte import PRINCIPES_VISUELS, presentation_plateforme
from .compliance import disclaimer_for
from .formats import get_format
import json


def brief(platform: str, title: str, concept_id: str, source: str, policy: dict | None = None) -> str:
    fmt = get_format(platform)
    beats = "\n".join(
        f"- {index}. {beat.id} — {beat.intent}"
        for index, beat in enumerate(fmt.beats, 1)
    )
    visuals = "\n".join(f"- {rule}" for rule in PRINCIPES_VISUELS)
    policy_text = json.dumps(policy or {}, ensure_ascii=False, indent=2)
    return f"""Tu produis l'unique script face caméra BRITED Studio. Mikael le prononcera lui-même devant un micro et une caméra. Ce même texte servira sur Instagram, TikTok, YouTube Shorts et Facebook.

SUJET : {title}
IDENTIFIANT : {concept_id}

SOURCE DE VÉRITÉ ABSOLUE :
{source}

POLITIQUE ÉDITORIALE VALIDÉE — À RESPECTER INTÉGRALEMENT :
{policy_text}

RÈGLES FACTUELLES :
- N'utilise que les faits, chiffres, dates et articles présents dans la source.
- N'invente rien et ne transforme pas un cas simplifié en règle générale.
- Conserve la condition d'application, l'exception utile et un exemple parlant.
- Traite un seul angle précis et une seule règle principale par vidéo.
- Supprime seulement les répétitions inutiles ; ne raccourcis jamais une condition, une réserve, un chiffre, un exemple nécessaire ou une source pour tenir une durée.
- Si le sujet complet exige plusieurs règles principales, sélectionne le sous-angle annoncé par le titre et réserve les autres mécanismes à une mini-série, sans les évoquer partiellement.
- Si la source ne suffit pas, réponds uniquement SOURCE INSUFFISANTE.
- Ne donne aucune recommandation personnalisée.
- Pour tout sujet Finance portant sur un produit précis, nomme explicitement dès le titre ou l'accroche la nature exacte du contrat, du compte, du support ou du produit concerné. N'écris jamais seulement « votre contrat » ou « ce contrat » si son type n'apparaît pas dans la même phrase. Si la source explique un mécanisme général sans produit particulier, nomme précisément ce mécanisme sans lui inventer un support absent de la fiche source.

MISSION PÉDAGOGIQUE — COMPRÉHENSION À LA PREMIÈRE ÉCOUTE :
- Écris pour une personne qui ne connaît rien à la gestion de patrimoine. Aucun savoir préalable n'est supposé.
- Pars d'une situation de vie reconnaissable : argent placé, couple, enfant, logement, retraite, impôt, succession ou erreur du quotidien.
- Donne une explication complète et utile avant le CTA. Ne garde jamais une information essentielle pour forcer la prise de rendez-vous.
- Construis un mini-apprentissage : situation concrète → règle en mots simples → exemple → point pratique à vérifier → CTA sans pression.
- Dans l'exemple, fais vivre la situation au spectateur : « Imaginez que vous… », « Prenons votre cas » ou « Si vous… ». Adapte la tournure au sujet et varie-la d'une vidéo à l'autre ; ne récite pas systématiquement la même amorce.
- Si un terme technique est indispensable, explique-le immédiatement avec des mots courants. Exemple : « une soulte, c'est une somme d'argent ajoutée à l'échange ».
- Le spectateur doit pouvoir résumer la vidéo en une phrase après une seule écoute.
- Fais sentir l'expertise par la clarté et la précision, pas par l'accumulation de jargon, d'articles ou de chiffres.
- La finalité est de créer dans la durée une audience de confiance et un vivier de clients potentiels. Le contenu reste néanmoins utile à celui qui ne prendra jamais rendez-vous.
- La conclusion suit le mode du calendrier : idée utile sans invitation, discussion, enregistrement, abonnement ou contact discret. La communauté est prioritaire ; aucun rendez-vous systématique.
- Le compte accueille salariés cadres ou non, professions libérales et chefs d’entreprise. Chaque vidéo vise une situation précise, sans énumérer tous les publics.
- Mikael est conseiller en gestion de patrimoine : accompagnement juridique et fiscal, conseil en investissement immobilier et financier. Ne lui invente aucun résultat, témoignage ou spécialité.
- Zéro ou une invitation, sans urgence artificielle, peur ni promesse. Ne sollicite pas de données personnelles en commentaire.

SIMPLICITÉ PRIORITAIRE :
- Une vidéo répond à une question du quotidien. Ne transforme pas la fiche source en cours condensé.
- Donne une réponse compréhensible dès le début ; une question simple et honnête peut suffire comme accroche.
- Aucun mot technique non expliqué. Préfère « part du logement » à « quote-part » et « valeur du placement » à « valeur liquidative ».
- N'ajoute pas plusieurs mécanismes, chiffres ou exceptions secondaires pour montrer ton expertise.
- Conserve les conditions qui changent la réponse. Si elles sont trop nombreuses, resserre la question plutôt que de les masquer.
- La dernière phrase peut simplement donner une idée à retenir, sans commentaire, abonnement ni rendez-vous.
- Ne remplace jamais un mot technique par un autre terme fiscal de sens différent.

NATUREL ORAL FACE CAMÉRA :
{presentation_plateforme(fmt.id)}
Format validé le 11 septembre 2026 : vidéo de 60 à 65 secondes, cible 63 secondes. Préparer environ 150 à 165 mots prononcés, nombres développés, à un débit naturel autour de 160 mots/minute avec des pauses. Ce budget est indicatif : chronométrer la lecture puis le montage final, jingle compris. Si un jingle est ajouté, déduire sa durée du budget de parole ; ne pas accélérer artificiellement. Un texte seul ne garantit pas la durée réelle ni une rémunération TikTok.
Parle comme à un ami en le vouvoyant : vous, votre, vos. Une situation familière, une seule idée, un exemple concret avec les chiffres utiles, une explication de ce que cela change pour lui et une conclusion utile. Pas de dialogue fictif à deux voix, pas de témoignage inventé, pas de tic systématique comme imaginez ou vous voyez.
- Les deux premières secondes doivent arrêter le défilement. Commence directement par une tension concrète pour le spectateur : argent perdu, erreur fréquente, risque, choix surprenant, chiffre utile ou question qui le concerne personnellement.
- L'accroche fait idéalement 8 à 16 mots et ne dépasse jamais 18 mots. Elle ne commence jamais par « Aujourd'hui », « Dans cette vidéo », « Nous allons voir », « Je vais vous expliquer », « Parlons de » ou « Il faut savoir que ».
- N'annonce pas le thème comme dans un cours : crée immédiatement une raison de rester, puis apporte une première réponse ou une première valeur dès la phrase suivante.
- La deuxième phrase n'est jamais une question et ne reformule jamais le hook. Elle répond nettement ou révèle immédiatement la conséquence essentielle.
- Toute question doit être idiomatique à l'oral. Écris « déclenche-t-il un impôt ? » ou « est-ce imposable ? », jamais une formule maladroite comme « cela vous impose ? ».
- Chaque phrase doit faire progresser le spectateur : révélation, règle utile, conséquence concrète, exemple ou réserve indispensable. Supprime toute transition décorative.
- Le rythme recherché est : hook percutant → réponse nette → explication rapide → exemple parlant → réserve courte et posée → conclusion naturelle et utile.
- Utilise majoritairement des phrases de 6 à 18 mots. Une idée par phrase. Évite les paragraphes magistraux, les longues définitions et les énumérations de cours.
- Préfère un mot courant à un terme professionnel : « somme ajoutée » avant « soulte », « somme retirée avant le calcul de l’impôt » avant « abattement », « base de calcul » avant « assiette ». Quand le terme légal doit être conservé, donne d'abord sa traduction simple.
- Écris comme Mikael parlerait à une seule personne, jamais comme un article, une voix off ou une notice.
- Chaque phrase doit pouvoir être dite d'un seul souffle raisonnable. Alterne phrases courtes et phrases moyennes.
- Une phrase prononcée ne dépasse jamais 35 mots. Si plusieurs chiffres ou conditions sont nécessaires, fais deux ou trois phrases naturelles au lieu d'une énumération au point-virgule.
- Utilise seulement des liaisons orales utiles : « Concrètement », « Prenons un exemple », « Mais attention ». Pas de tic de langage artificiel.
- Adresse-toi directement au spectateur avec « vous ». Privilégie les verbes et la voix active.
- Donne au discours une personnalité humaine et complice : Mikael parle à une personne, pas à une audience abstraite. L'exemple doit contenir une projection explicite du spectateur dans la situation, avec « vous », « votre » ou « vos ».
- L'accroche doit sonner spontanée, vive et spécifique ; la réponse doit arriver sans suspense fabriqué.
- L'exemple doit se raconter facilement. La réserve est plus posée, mais reste fluide.
- Lis mentalement chaque phrase à voix haute avant de la rendre. Toute tournure qui sonne « texte écrit » doit être reformulée.
- N'insère aucune indication scénique ni libellé éditorial dans le texte prononcé. « La question : », « La réponse : » et « La règle : » sont interdits. Place les intentions dans une colonne séparée.

REPÈRES DE PROGRESSION : les beats structurent la préparation, pas un cours récité. L'exemple peut porter l'explication ; les raccords restent naturels.
ORDRE DES BEATS POUR LE TABLEAU :
{beats}

PRÉSENTATION FACE CAMÉRA :
- Mikael reste le sujet principal de l'image.
- Les incrustations servent uniquement à afficher les chiffres, mots-clés, conditions et sources utiles.
- Aucun écran graphique ne doit dicter le rythme de la parole.

ADÉQUATION AU GABARIT :
- Écris d'abord pour la compréhension orale, puis pour l'écran vertical validé.
- Dans « Texte écran », utilise exclusivement les chiffres pour les nombres, € à la place du mot euros, K€ si utile, % pour les taux et JJ/MM/AAAA pour les dates. La narration reste écrite pour une prononciation française naturelle et complète.
- Dans « Texte écran », écris la relation inférieur ou égal sous la forme =< ; dans la narration, écris et fais prononcer « inférieur ou égal » en toutes lettres.
- Une seule production éditoriale existe : le script face caméra certifié alimente à l'identique YouTube, Instagram, TikTok et Facebook.
- La question doit être autonome, lisible et entièrement prononcée avant la réponse.
- La réponse doit commencer sur une page distincte et rester courte.
- Ne compresse jamais une réserve juridique ou fiscale pour éviter une page supplémentaire ou atteindre artificiellement la durée.
- Si une idée dépasse la capacité d'une page, conserve une phrase naturelle : l'agent de format la répartira sans supprimer ni reformuler aucun mot.

FORMAT MARKDOWN OBLIGATOIRE :
# Titre
**Plateforme** : {fmt.label}
**Durée cible** : 60–65 secondes (viser 63 secondes)
**Durée estimée** : ... (hypothèse de débit et pauses explicites ; lecture chronométrée à confirmer)
| # | Beat | Narration | Visuel | Texte écran |
Une ligne par beat, exactement dans l'ordre imposé.
## Narration continue
Texte complet, identique à la concaténation des narrations du tableau.
## Guide de tournage
Pour chaque beat : intention, accent à placer et respiration naturelle. Ce guide n'est jamais prononcé.
## Incrustations
Liste minimale des textes à ajouter au montage, sans recopier tout le discours.
## Légende
## Hashtags
## Sources
Liens officiels issus uniquement de la fiche source.
## Mention
{disclaimer_for(fmt.id)}
"""
