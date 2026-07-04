# Registre RGPD et protection des données — Bloc 1

## 1. Objectif

Ce document présente la prise en compte du RGPD dans le cadre du projet **PayLive AI Copilot**.

Le projet manipule des données simulées représentant l’activité d’une solution d’aide à la vente en live shopping.

Même si aucune donnée réelle de l’entreprise PayLive n’est utilisée, le projet contient des champs qui pourraient être considérés comme des données personnelles dans un contexte réel.

Ce document permet donc de décrire :

- les traitements de données prévus ;
- les catégories de données utilisées ;
- les finalités du traitement ;
- les personnes concernées ;
- les mesures de minimisation ;
- les mesures de sécurité ;
- les durées de conservation prévues ;
- les droits des personnes ;
- les précautions prises dans le projet.

## 2. Rappel du contexte projet

Le projet **PayLive AI Copilot** consiste à construire un assistant intelligent pour les vendeurs qui réalisent des lives sur des plateformes comme TikTok ou Instagram.

L’objectif métier est d’aider un vendeur à :

- analyser les commentaires d’un live ;
- détecter les intentions d’achat ;
- suivre les paniers ;
- suivre les commandes ;
- suivre les paiements ;
- analyser la performance commerciale d’un live ;
- préparer un dataset exploitable pour de futures fonctionnalités IA.

Les données utilisées dans ce projet sont entièrement simulées ou issues de sources externes sans lien avec de vraies données PayLive.

## 3. Absence de données réelles PayLive

Aucune donnée réelle de l’entreprise PayLive n’est utilisée.

Le projet utilise uniquement :

```text
données simulées
données fictives
produits issus d’une API publique
produits issus d’un site de scraping autorisé pour l’entraînement
événements générés artificiellement
```

Les données personnelles présentes dans les fichiers sont donc fictives.

Exemples :

```text
noms de vendeurs fictifs
emails fictifs
numéros de téléphone fictifs
usernames fictifs
commentaires simulés
références de transaction fictives
```

## 4. Données personnelles potentielles

Même si les données sont fictives, certains champs correspondent à des catégories de données personnelles dans un contexte réel.

## 4.1. Données vendeurs

Tables concernées :

```text
core.sellers
data/processed/sellers_clean.csv
```

Données personnelles potentielles :

```text
owner_first_name
owner_last_name
email
phone_number
country
```

Ces données peuvent permettre d’identifier directement ou indirectement un vendeur dans un contexte réel.

## 4.2. Données clients

Tables concernées :

```text
core.customers
data/processed/customers_clean.csv
```

Données personnelles potentielles :

```text
username
email
country
platform
```

Dans un contexte réel, un username ou un email peut permettre d’identifier un utilisateur.

## 4.3. Commentaires live

Tables concernées :

```text
core.live_comments
data/processed/live_comments_clean.csv
```

Données personnelles potentielles :

```text
username
comment_text
commented_at
comment_language
manual_intent_label
extracted_product_keyword
```

Le contenu d’un commentaire peut contenir des informations personnelles si un utilisateur y écrit des détails personnels.

Dans le projet, les commentaires sont simulés.

## 4.4. Données de paiement

Tables concernées :

```text
core.payments
data/processed/payments_clean.csv
```

Données sensibles potentielles :

```text
payment_provider
payment_status
payment_method
transaction_reference
paid_at
```

Le projet ne stocke aucune donnée bancaire réelle.

Il ne contient pas :

```text
numéro de carte bancaire
IBAN
cryptogramme
adresse de facturation réelle
données bancaires nominatives
```

Les références de transaction sont fictives.

## 4.5. Événements live

Tables concernées :

```text
core.live_events
data/processed/live_events_clean.csv
```

Données potentielles :

```text
customer_id
event_type
event_timestamp
event_value
source_system
```

Dans un contexte réel, des logs d’événements peuvent être rattachés à un utilisateur.

Dans le projet, les identifiants clients sont simulés.

## 5. Finalités du traitement

Les finalités du traitement sont les suivantes :

```text
préparer un dataset exploitable pour l’analyse métier
stocker les données nettoyées dans PostgreSQL
exposer les données via une API REST
analyser la performance des lives
préparer les futures fonctionnalités IA
suivre les paniers, commandes et paiements simulés
détecter les intentions d’achat dans les commentaires simulés
```

Le traitement n’a pas pour objectif de surveiller de vraies personnes.

Le traitement n’a pas pour objectif de prendre une décision automatisée réelle sur des utilisateurs.

## 6. Base légale dans le contexte du projet

Dans le cadre du dossier professionnel, les données sont simulées.

Le projet n’effectue donc pas de traitement opérationnel sur des personnes réelles.

Dans un contexte réel, la base légale devrait être déterminée par l’entreprise responsable du traitement.

Bases légales possibles selon le cas réel :

```text
exécution d’un contrat
intérêt légitime
consentement
obligation légale pour certaines traces comptables ou transactionnelles
```

Cette analyse devrait être validée par un DPO ou un responsable conformité dans un projet réel.

## 7. Personnes concernées

Dans un contexte réel, les personnes concernées pourraient être :

```text
vendeurs
clients
spectateurs des lives
utilisateurs ayant commenté
utilisateurs ayant créé un panier
utilisateurs ayant passé une commande
```

Dans ce projet, aucune personne réelle n’est concernée.

## 8. Responsable de traitement

Dans le cadre du projet scolaire :

```text
Projet : PayLive AI Copilot
Nature : projet de dossier professionnel
Responsable technique : étudiant développeur IA
Données : simulées et fictives
```

Dans un contexte réel, le responsable de traitement serait l’organisation qui détermine les finalités et les moyens du traitement.

## 9. Sous-traitants et outils techniques

Les outils utilisés dans le projet sont :

```text
Python
Pandas
PostgreSQL
Docker
pgAdmin
FastAPI plus tard pour l’API
fichiers CSV
```

Ces outils sont utilisés en local dans le cadre du projet.

Aucun transfert de données personnelles réelles vers un service tiers n’est effectué.

## 10. Principe de minimisation

Le projet applique le principe de minimisation.

Seules les données nécessaires à la démonstration technique sont conservées.

Exemples de minimisation :

```text
le dataset final IA ne contient pas les emails clients
le dataset final IA ne contient pas les numéros de téléphone
le dataset final IA ne contient pas les commentaires détaillés
le dataset final IA ne contient pas les références de transaction
le dataset final travaille au niveau agrégé par live
```

Le fichier principal :

```text
data/processed/dataset_final_live_sales.csv
```

contient une ligne par live et non une ligne par personne.

Cette approche réduit l’exposition des données personnelles.

## 11. Séparation des données

La base PostgreSQL est organisée en trois schémas :

```text
core
analytics
audit
```

## 11.1. Schéma `core`

Le schéma `core` contient les tables métiers détaillées :

```text
core.sellers
core.customers
core.live_comments
core.payments
```

Certaines de ces tables peuvent contenir des données personnelles potentielles dans un contexte réel.

## 11.2. Schéma `analytics`

Le schéma `analytics` contient le dataset final agrégé :

```text
analytics.dataset_final_live_sales
```

Ce schéma est moins exposé aux données personnelles car il contient des indicateurs agrégés par live.

## 11.3. Schéma `audit`

Le schéma `audit` contient les traces techniques :

```text
audit.import_batches
audit.import_logs
```

Ces tables permettent de tracer les imports.

## 12. Pseudonymisation

Le projet utilise des identifiants fictifs :

```text
seller_id
customer_id
live_id
cart_id
order_id
payment_id
event_id
```

Ces identifiants ne correspondent pas à des personnes réelles.

Dans un contexte réel, l’utilisation d’identifiants techniques permettrait de limiter l’exposition directe des personnes.

Exemple :

```text
customer_id = CUST_001
```

au lieu de stocker systématiquement le nom complet du client.

## 13. Anonymisation

Le dataset final agrégé se rapproche d’une logique d’anonymisation partielle car il ne contient pas les commentaires détaillés, emails ou numéros de téléphone.

Cependant, dans un contexte réel, il faudrait vérifier que les données agrégées ne permettent pas de réidentifier une personne.

Dans ce projet, les données étant simulées, le risque de réidentification est nul.

## 14. Données conservées dans le dataset final

Le dataset final contient principalement des indicateurs agrégés :

```text
total_comments
purchase_intent_comments
total_carts
paid_carts
total_orders
total_revenue
payment_success_rate
conversion_rate
api_error_events
top_product_category
```

Il conserve aussi :

```text
live_id
seller_id
platform
live_date
shop_name
```

Ces informations servent à l’analyse métier et à la future API.

## 15. Données exclues du dataset final

Le dataset final ne contient pas :

```text
email vendeur
téléphone vendeur
email client
username client
commentaire détaillé
référence de transaction
méthode de paiement détaillée
```

Cette exclusion permet de limiter les données personnelles dans la partie analytique.

## 16. Durée de conservation

Dans le cadre du projet scolaire, les données sont conservées uniquement pendant la durée nécessaire à la réalisation du dossier.

Durée prévue :

```text
durée du projet et de l’évaluation
```

Dans un contexte réel, les durées de conservation devraient être définies selon :

```text
la finalité du traitement
les obligations légales
les besoins opérationnels
les obligations comptables
les règles internes de l’entreprise
```

Exemple de logique possible :

```text
logs techniques : durée limitée
données de commande : durée liée aux obligations commerciales ou comptables
données analytiques agrégées : durée plus longue si elles ne permettent pas l’identification
```

## 17. Sécurité des données

Les mesures de sécurité appliquées dans le projet sont :

```text
utilisation d’un fichier .env pour les paramètres de connexion
absence de données réelles
base PostgreSQL isolée dans Docker
séparation des schémas core, analytics et audit
contrôle qualité après import
logs techniques d’import
documentation des traitements
```

Le fichier `.env` ne doit pas être versionné si des identifiants sensibles y sont stockés.

Le fichier `.env.example` sert uniquement de modèle.

## 18. Gestion des accès

Les accès prévus dans le projet sont simples :

```text
postgres : administration locale
future API : accès lecture contrôlé
analytics : accès lecture pour les futurs traitements IA
```

Dans un contexte réel, il faudrait créer des utilisateurs séparés :

```text
admin_db
api_user
analytics_user
```

Principe recommandé :

```text
un utilisateur technique ne doit avoir que les droits nécessaires à son usage
```

## 19. Journalisation et traçabilité

Le projet conserve des traces techniques.

Exemples :

```text
logs/import_processed_data.log
logs/check_database_quality.log
data/processed/database_import_report.csv
data/processed/database_import_summary.csv
data/processed/database_quality_summary.csv
```

En base, les tables suivantes conservent les informations d’import :

```text
audit.import_batches
audit.import_logs
```

Ces éléments permettent de prouver :

```text
quand les données ont été importées
quels fichiers ont été importés
combien de lignes ont été insérées
si l’import a réussi
si des erreurs ont eu lieu
```

## 20. Droits des personnes

Dans un contexte réel, les personnes concernées disposeraient de droits sur leurs données.

Droits principaux :

```text
droit d’accès
droit de rectification
droit à l’effacement
droit d’opposition
droit à la limitation
droit à la portabilité selon les cas
```

Dans ce projet, ces droits ne sont pas exercés car aucune donnée réelle n’est utilisée.

Cependant, la structure de la base permettrait d’identifier les données rattachées à un client via :

```text
customer_id
```

Exemples de tables concernées :

```text
core.customers
core.live_comments
core.carts
core.orders
core.live_events
```

## 21. Exemple de suppression ou anonymisation future

Dans un contexte réel, si un client demande la suppression de ses données, il faudrait définir une procédure.

Exemple de logique possible :

```text
identifier le customer_id
anonymiser le username
supprimer ou anonymiser l’email
anonymiser les commentaires
conserver uniquement les données obligatoires si nécessaire
mettre à jour les logs de traitement
```

Les données agrégées du dataset final pourraient être conservées si elles ne permettent plus d’identifier la personne.

## 22. Analyse des risques

Risques potentiels dans un contexte réel :

```text
identification d’un client via son email
identification d’un client via son username
présence d’informations personnelles dans un commentaire
accès non autorisé à la base
conservation excessive des données
exposition d’identifiants dans un dépôt Git
utilisation abusive des données analytiques
```

Mesures prévues dans le projet :

```text
données fictives
minimisation dans le dataset final
séparation core / analytics / audit
fichier .env séparé
documentation des traitements
contrôle qualité des imports
absence de données bancaires réelles
```

## 23. Matrice des traitements

| Traitement | Données concernées | Finalité | Personnes concernées | Schéma | Mesures |
|---|---|---|---|---|---|
| Gestion des vendeurs | seller_id, shop_name, email fictif, téléphone fictif | Identifier les vendeurs simulés | Vendeurs fictifs | core | Données fictives, nettoyage, minimisation |
| Gestion des clients | customer_id, username, email fictif | Simuler les interactions clients | Clients fictifs | core | Pseudonymisation, données fictives |
| Analyse des commentaires | comment_text, intent_label | Détecter les intentions d’achat | Clients fictifs | core | Commentaires simulés, nettoyage |
| Gestion des paniers | cart_id, customer_id, live_id | Suivre les paniers simulés | Clients fictifs | core | Identifiants techniques |
| Gestion des commandes | order_id, cart_id, montant | Suivre les commandes simulées | Clients fictifs | core | Données simulées |
| Gestion des paiements | payment_id, transaction_reference fictive | Suivre les paiements simulés | Clients fictifs | core | Aucune donnée bancaire réelle |
| Analyse finale IA | indicateurs agrégés par live | Préparer les futures analyses IA | Données agrégées | analytics | Minimisation, agrégation |
| Audit d’import | logs techniques | Tracer les imports | Administrateur technique | audit | Logs techniques limités |

## 24. Registre simplifié des activités de traitement

## 24.1. Traitement : préparation et analyse des données live shopping

| Champ | Description |
|---|---|
| Nom du traitement | Préparation et analyse des données live shopping |
| Responsable | Projet PayLive AI Copilot |
| Finalité | Préparer des données propres et agrégées pour l’analyse et l’IA |
| Données traitées | Vendeurs, clients fictifs, commentaires simulés, paniers, commandes, paiements simulés |
| Personnes concernées | Vendeurs fictifs, clients fictifs |
| Base légale | Non applicable dans le projet car données simulées |
| Source des données | Données générées, API publique, scraping autorisé, base simulée |
| Destinataires | Application locale, base PostgreSQL, future API |
| Durée de conservation | Durée du projet |
| Mesures de sécurité | Docker, `.env`, séparation des schémas, logs, données fictives |
| Transfert hors UE | Aucun transfert |
| Données sensibles | Aucune donnée sensible réelle |

## 24.2. Traitement : dataset final analytique

| Champ | Description |
|---|---|
| Nom du traitement | Dataset final analytique live sales |
| Finalité | Produire un dataset agrégé prêt pour la future IA |
| Table concernée | analytics.dataset_final_live_sales |
| Granularité | Une ligne par live |
| Données personnelles | Très limitées, pas d’email, pas de téléphone, pas de commentaire détaillé |
| Mesures | Agrégation, minimisation, indicateurs synthétiques |
| Statut | ready_for_ai |

## 25. Justification des choix RGPD dans le projet

Les choix réalisés dans le projet permettent de limiter les risques :

```text
aucune donnée réelle PayLive
données simulées et fictives
pas de données bancaires réelles
agrégation par live
suppression des emails invalides
usernames manquants remplacés par anonymous_user
dataset final sans commentaires détaillés
séparation entre données détaillées et données analytiques
documentation des traitements
```

Ces choix sont cohérents avec les principes de minimisation, de limitation des finalités et de sécurité.

## 26. Limites

Ce document est adapté au cadre d’un projet de dossier professionnel.

Il ne remplace pas une analyse juridique complète.

Dans un contexte réel, il faudrait compléter ce travail avec :

```text
validation par un DPO
analyse d’impact si nécessaire
mentions d’information aux utilisateurs
politique de conservation détaillée
gestion effective des droits utilisateurs
revue de sécurité
contrats de sous-traitance éventuels
```

## 27. Lien avec les autres documents du projet

Ce document complète :

```text
docs/14_modelisation_base_donnees.md
docs/15_creation_base_donnees_postgresql.md
docs/16_import_donnees_postgresql.md
docs/17_controle_qualite_base_donnees.md
```

Il justifie la prise en compte de la protection des données dans la conception, l’import et l’exploitation de la base PostgreSQL.

## 28. Conclusion

La prise en compte du RGPD dans le projet PayLive AI Copilot repose sur une approche de minimisation et de simulation.

Le projet ne manipule aucune donnée réelle de PayLive.

Les données personnelles potentielles sont fictives, limitées et séparées des données analytiques.

Le dataset final IA est agrégé par live et ne contient pas les informations personnelles détaillées des clients.

Cette approche permet de construire un pipeline de données réaliste tout en limitant les risques liés aux données personnelles.