# Collecte depuis une base de données SQL — Bloc 1

## 1. Objectif

Cette étape a pour objectif d’automatiser l’extraction de données depuis une base de données SQL.

Dans le cadre du projet PayLive AI Copilot, aucune base réelle de l’entreprise n’est utilisée. Une base SQL source simulée est donc créée afin de représenter un ancien système transactionnel.

## 2. Base source simulée

La base source simulée est :

`data/raw/legacy_database/paylive_legacy.db`

Elle utilise SQLite pour faciliter l’exécution du projet sans dépendance externe.

## 3. Script utilisé

Le script utilisé est :

`src/data_collection/collect_from_database.py`

## 4. Tables source créées

Les tables source créées sont :

- `legacy_sellers`
- `legacy_customers`
- `legacy_live_sessions`
- `legacy_carts`
- `legacy_orders`
- `legacy_payments`

Ces tables sont alimentées à partir des fichiers CSV bruts générés précédemment.

## 5. Requêtes SQL d’extraction

Les requêtes SQL sont documentées dans :

`sql/04_extraction_queries.sql`

Elles permettent d’extraire :

- les vendeurs ;
- les sessions live ;
- les commandes payées ;
- le chiffre d’affaires par live ;
- les commandes incomplètes.

## 6. Traitements réalisés

Le script réalise les actions suivantes :

- création d’une base SQL source simulée ;
- connexion programmatique à la base ;
- import des fichiers CSV bruts dans des tables SQL ;
- exécution de requêtes SQL d’extraction ;
- utilisation de jointures entre commandes, paiements, paniers, lives et vendeurs ;
- utilisation de filtres sur les statuts de paiement ;
- utilisation d’agrégations pour calculer le chiffre d’affaires ;
- sauvegarde des résultats d’extraction en CSV ;
- génération d’un manifeste ;
- génération d’un rapport de schéma ;
- génération d’un rapport d’exécution des requêtes ;
- journalisation de l’exécution.

## 7. Sorties générées

Les sorties générées sont :

- `data/raw/legacy_database/paylive_legacy.db`
- `data/interim/database_extracts/legacy_sellers_extract.csv`
- `data/interim/database_extracts/legacy_live_sessions_extract.csv`
- `data/interim/database_extracts/paid_orders_with_payments_extract.csv`
- `data/interim/database_extracts/revenue_by_live_extract.csv`
- `data/interim/database_extracts/incomplete_orders_extract.csv`
- `data/interim/database_extraction_manifest.csv`
- `data/interim/database_extraction_schema_report.csv`
- `data/interim/database_extraction_query_report.csv`
- `data/interim/database_import_report.csv`
- `data/interim/database_extraction_errors.csv`
- `logs/collect_from_database.log`

## 8. Justification

Cette étape permet de démontrer la capacité à extraire des données depuis une base SQL.

Elle complète les autres sources de collecte : fichiers CSV, API REST et scraping web.

## 9. Limite

La base utilisée est simulée et ne représente pas l’activité réelle de l’entreprise.

Cependant, elle permet de reproduire un scénario réaliste d’extraction depuis un ancien système transactionnel.