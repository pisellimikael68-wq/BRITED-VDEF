---
id: cryptoactifs_fiscalite_cessions
titre: Échanger une crypto contre une autre n'est pas imposable
domaine: cryptoactifs
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 9
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [crypto, bitcoin, actifs numériques, plus-value crypto]
resume: >-
  Seule la conversion en monnaie ayant cours légal ou l'achat d'un bien
  déclenche l'imposition. Les échanges entre actifs numériques sont neutres.
  Les comptes détenus à l'étranger doivent être déclarés.
sources:
  - type: texte_legal
    ref: CGI, article 150 VH bis
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041464958
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: CGI, article 1649 bis C (déclaration des comptes d'actifs numériques)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037992141
    consulte_le: 2026-07-27
  - type: bofip
    ref: BOI-RPPM-PVBMC-30
    url: https://bofip.impots.gouv.fr/doctrine/BOI-RPPM-PVBMC-30
    consulte_le: 2026-07-27
chiffres:
  - cle: Taux d'imposition des plus-values
    valeur: "30"
    unite: "%"
    source: 0
  - cle: Seuil annuel de cessions en dessous duquel il n'y a pas d'imposition
    valeur: "305"
    unite: "€"
    source: 0
  - cle: Imposition d'un échange crypto contre crypto
    valeur: "0"
    unite: "€"
    source: 0
  - cle: Amende par compte étranger non déclaré
    valeur: "750"
    unite: "€"
    source: 1
    commentaire: par compte et par année non déclarée, CGI article 1736 X, vérifié le 2026-07-27
relations:
  regi_par:
    - compte_titres_pfu
  alternative_a:
    - or_fiscalite_metaux_precieux
  en_conflit_avec:
    - fiscalite_internationale_residence
erreurs_frequentes:
  - Croire que chaque échange entre cryptos déclenche un impôt. Seule la sortie vers une monnaie légale ou l'achat d'un bien est imposable.
  - Oublier de déclarer les comptes ouverts sur des plateformes étrangères, ce qui expose à une amende par compte et par an.
  - Croire que l'anonymat protège. Les plateformes européennes transmettent les informations à l'administration.
  - Calculer la plus-value opération par opération. La méthode légale porte sur la valeur globale du portefeuille.
questions_clients:
  - Dois-je déclarer si je n'ai rien vendu en euros ?
  - Mon compte sur une plateforme étrangère doit-il être déclaré ?
  - Comment calculer ma plus-value ?
a_ne_pas_dire:
  - Ne jamais inciter à l'achat d'actifs numériques : la promotion est encadrée par la loi du 9 juin 2023.
  - Toujours rappeler le risque de perte totale en capital.
---

## Le mécanisme

L'article 150 VH bis du CGI n'impose que les cessions à titre onéreux d'actifs
numériques **contre une monnaie ayant cours légal** ou contre un bien ou service.
Les échanges entre actifs numériques sont expressément neutres : ils ne
constituent pas un fait générateur.

Le taux est de 30 %, identique au prélèvement forfaitaire unique.

## Ce qui se joue vraiment

Un portefeuille qui tourne entre plusieurs actifs pendant des années ne génère
aucune imposition tant qu'aucun euro n'en sort. L'impôt se déclenche à la
sortie, et se calcule sur la valeur globale du portefeuille au moment de la
cession, non opération par opération.

En dessous de 305 € de cessions imposables sur l'année, aucune imposition
n'est due.

## Le point de vigilance

La déclaration des comptes détenus sur des plateformes établies à l'étranger
est obligatoire, indépendamment de toute plus-value. L'amende s'applique par
compte non déclaré et par année. C'est le manquement le plus fréquent et le
plus facilement détecté, les plateformes européennes transmettant désormais les
informations à l'administration.
