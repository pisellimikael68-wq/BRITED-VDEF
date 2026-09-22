---
id: sci_apport_ou_acquisition
titre: Apporter un bien à une SCI ou l'acheter par elle
domaine: sci
type: strategie
statut: valide
difficulte: avance
potentiel_viral: 7
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
  - apport immeuble SCI
  - créer une SCI pour un bien déjà acheté
  - coût apport SCI
resume: >-
  Faire acheter un bien par la SCI dès l'origine coûte les droits de mutation
  une seule fois. Apporter un bien déjà détenu à une SCI créée après coup
  déclenche une seconde taxation et, si la société est à l'impôt sur les
  sociétés, l'imposition de la plus-value d'apport.
sources:
  - type: texte_legal
    ref: CGI, article 810 (droits d'apport)
  - type: texte_legal
    ref: CGI, article 809, I bis (apport d'immeuble à une société soumise à l'IS)
  - type: texte_legal
    ref: CGI, article 1594 D (droits de mutation à titre onéreux sur les immeubles)
  - type: texte_legal
    ref: Code civil, article 1832 (constitution de la société)
chiffres:
  - cle: Nombre d'associés minimum d'une SCI
    valeur: "2"
    source: 3
  - cle: Ordre de grandeur des droits de mutation sur une acquisition immobilière
    valeur: "5 à 6"
    unite: "%"
    source: 2
    commentaire: taux départemental, à vérifier pour le département concerné
relations:
  regi_par:
    - sci_is_ou_ir
  complete_par:
    - sci_compte_courant_associe
    - immobilier_achat_couple_non_marie
erreurs_frequentes:
  - Créer la SCI après avoir acheté. L'apport ultérieur fait payer une seconde fois des droits sur le même bien.
  - Croire que l'apport est neutre fiscalement. Il ne l'est pas quand la société relève de l'impôt sur les sociétés : la plus-value latente devient imposable.
  - Oublier que l'apport d'un bien grevé d'un emprunt est un apport à titre onéreux à hauteur du passif repris, avec un régime propre.
  - Créer une SCI pour un bien unique occupé par les associés, sans mesurer que la société ne peut pas bénéficier de l'exonération de plus-value de la résidence principale dans les mêmes conditions qu'un particulier.
questions_clients:
  - J'ai déjà l'appartement, puis-je le mettre dans une SCI ?
  - Combien coûte la création d'une SCI ?
  - Faut-il une SCI pour acheter à deux ?
a_ne_pas_dire:
  - Ne jamais dire au spectateur de créer une SCI : la structure engage la fiscalité, la responsabilité des associés et la transmission. Chiffrer le coût sur un cas fictif reste permis.
  - Ne pas présenter la SCI comme un outil d'optimisation fiscale : c'est d'abord un outil d'organisation juridique.
---

## Le mécanisme

Deux chemins mènent au même résultat apparent — un immeuble détenu par une SCI —
avec des coûts très différents.

**La SCI achète directement.** Elle se constitue avant l'acquisition, obtient
son financement et signe chez le notaire. Les droits de mutation sont dus une
fois, comme pour n'importe quel acheteur.

**L'associé apporte un bien qu'il possède déjà.** L'opération est un transfert
de propriété : elle est taxée à son tour. Le bien a donc supporté les droits
deux fois, à l'achat initial puis à l'apport.

## Ce qui se joue vraiment

Le surcoût dépend surtout du régime fiscal de la société.

Si la SCI relève de l'impôt sur le revenu, l'apport pur et simple d'un immeuble
par une personne physique bénéficie d'un régime de faveur en matière de droits
d'apport.

Si elle relève de l'**impôt sur les sociétés**, l'apport fait sortir le bien du
patrimoine privé vers une sphère professionnelle : la plus-value latente devient
imposable au moment de l'apport, alors même qu'aucune somme n'a été encaissée.
C'est le point qui transforme une réorganisation apparemment neutre en note
fiscale immédiate.

## Le point de vigilance

L'apport d'un bien financé à crédit n'est pas un apport pur et simple. À hauteur
du passif repris par la société, il s'analyse en apport **à titre onéreux**,
c'est-à-dire en vente — avec les droits correspondants.

Enfin, la SCI n'est pas neutre sur la résidence principale. Un particulier qui
vend sa résidence principale est exonéré de plus-value ; une société ne
bénéficie pas du même régime dans les mêmes conditions. Loger sa résidence
principale dans une SCI est une décision qui se prend en connaissance de cette
différence, pas par réflexe.
### content/sci/compte_courant_associe.md
