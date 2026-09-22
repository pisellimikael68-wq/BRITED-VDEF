---
id: cryptoactifs_declaration_2086
titre: Remplir le formulaire 2086
domaine: cryptoactifs
type: notion
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
- déclaration crypto
- formulaire 2086
- déclarer ses comptes crypto
resume: Les cessions d'actifs numériques contre monnaie ayant cours légal se déclarent sur le formulaire
  2086, cession par cession. Les comptes ouverts à l'étranger se déclarent séparément, et l'omission de
  cette seconde obligation est sanctionnée par une amende forfaitaire.
sources:
- type: texte_legal
  ref: CGI, article 150 VH bis (plus-values de cession d'actifs numériques)
- type: texte_legal
  ref: CGI, article 1649 bis C (déclaration des comptes d'actifs numériques à l'étranger)
- type: texte_legal
  ref: CGI, article 1736, X (amende pour défaut de déclaration de compte)
- type: bofip
  ref: BOI-RPPM-PVBMC-30 (plus-values de cession d'actifs numériques)
  url: https://bofip.impots.gouv.fr/doctrine/BOI-RPPM-PVBMC-30
  consulte_le: 2026-07-29
chiffres:
- cle: Seuil annuel de cessions en deçà duquel la plus-value est exonérée
  valeur: '305'
  unite: €
  source: 0
  commentaire: prix total de cession sur l'année, pas le gain
- cle: Amende par compte étranger non déclaré
  valeur: '750'
  unite: €
  source: 2
  commentaire: portée à 1 500 € lorsque la valeur du compte dépasse 50 000 €
relations:
  regi_par:
  - cryptoactifs_fiscalite_cessions
  complete_par:
  - fiscalite_controle_fiscal
  alternative_a:
  - compte_titres_pfu
  s_applique_a:
  - impot_revenu_decote
  - impot_revenu_tranche_marginale
erreurs_frequentes:
- Croire que les échanges entre cryptoactifs sont imposables. Ils ne le sont pas: seule la conversion
    en monnaie ayant cours légal ou l'achat d'un bien déclenche l'imposition.
- Oublier de déclarer les comptes ouverts sur des plateformes étrangères, obligation distincte de la déclaration
  des plus-values et sanctionnée par une amende par compte et par an.
- Croire que le seuil de 305 € porte sur le gain. Il porte sur le montant total des cessions de l'année.
- Déclarer une plus-value globale sans détailler chaque cession, alors que le formulaire impose le calcul
  cession par cession avec la valeur globale du portefeuille.
questions_clients:
- Dois-je déclarer si je n'ai rien vendu ?
- Faut-il déclarer mon compte Binance ?
- Les échanges entre cryptos sont-ils taxés ?
a_ne_pas_dire:
- Ne pas laisser entendre qu'une plateforme étrangère échappe à l'administration — les échanges d'informations
  entre États se sont considérablement développés.
- Ne jamais calculer la plus-value réelle du spectateur. Un exemple de calcul sur des montants fictifs
  reste permis et souhaitable.
---

## Le mécanisme

Le régime de l'article 150 VH bis ne taxe pas la détention ni les arbitrages
entre actifs numériques. Le fait générateur est la **cession contre une monnaie
ayant cours légal**, ou l'utilisation des actifs pour acquérir un bien ou un
service.

Un portefeuille qui passe d'un actif à un autre cent fois dans l'année, sans
jamais revenir en euros, ne génère aucune imposition.

Le calcul se fait cession par cession, selon une formule qui rapporte le prix de
cession à la valeur globale du portefeuille au moment de l'opération, diminué du
prix total d'acquisition proportionnel. C'est ce calcul que le formulaire 2086
matérialise, ligne par ligne.

## Ce qui se joue vraiment

Deux obligations coexistent et sont régulièrement confondues.

La **déclaration des plus-values** passe par le 2086, annexé à la déclaration de
revenus, puis reportée sur la 2042 C.

La **déclaration des comptes d'actifs numériques ouverts à l'étranger** est une
obligation autonome, prévue par l'article 1649 bis C. Elle s'impose même si
aucune cession n'a été réalisée et même si le compte est vide, dès lors qu'il a
été ouvert, détenu ou clos dans l'année.

C'est cette seconde obligation qui produit les redressements les plus fréquents,
parce qu'elle est indépendante de tout gain : l'amende s'applique par compte et
par année non déclarée.

## Le point de vigilance

Le seuil de 305 € porte sur le **montant total des cessions** de l'année, pas
sur le gain. Un contribuable qui a cédé 2 000 € pour un gain de 40 € est dans le
champ, alors qu'il se croit sous le seuil.

La tenue d'un historique complet des opérations n'est pas facultative : sans
prix d'acquisition documenté, la plus-value se calcule sur une base
d'acquisition nulle, c'est-à-dire sur la totalité du prix de cession.
