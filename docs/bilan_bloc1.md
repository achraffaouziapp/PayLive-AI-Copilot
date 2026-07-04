# Bilan final du Bloc 1 — PayLive AI Copilot

## 1. Objectif du document

Ce document présente le bilan final du **Bloc 1** du projet **PayLive AI Copilot**.

Le Bloc 1 porte sur la capacité à :

```text
collecter des données depuis plusieurs sources
stocker les données préparées
mettre les données à disposition via une API REST
documenter les traitements
prendre en compte la qualité, la sécurité et le RGPD
```

Ce bilan permet de synthétiser :

```text
les travaux réalisés
les scripts développés
les documents produits
les preuves générées
les difficultés rencontrées
les corrections apportées
la couverture des compétences C1 à C5
```

## 2. Présentation synthétique du projet

**PayLive AI Copilot** est un projet d’assistant intelligent pour les vendeurs réalisant des ventes en live sur des plateformes comme TikTok Live ou Instagram Live.

L’objectif métier est de préparer un socle de données permettant ensuite de développer des fonctionnalités IA, comme :

```text
détection d’intention d’achat dans les commentaires
extraction de produit, taille, couleur ou quantité
suivi des paniers et commandes
analyse de performance des lives
recommandations commerciales
tableau de bord vendeur
```

Dans le Bloc 1, le projet se concentre sur le pipeline de données :

```text
collecte
qualité
nettoyage
agrégation
stockage
import
contrôle qualité
API REST
```

## 3. Données utilisées

Le projet n’utilise aucune donnée réelle de PayLive.

Les données utilisées sont :

```text
simulées
fictives
pseudonymisées
issues de sources externes autorisées
générées artificiellement
```

Les données contiennent volontairement des anomalies afin de démontrer les étapes de contrôle qualité et de nettoyage.

Exemples d’anomalies introduites :

```text
doublons
valeurs manquantes
emails invalides
statuts non normalisés
dates incohérentes
montants incorrects
clés étrangères invalides
valeurs numériques négatives
formats hétérogènes
```

## 4. Architecture globale réalisée

Le projet a été structuré de manière à séparer clairement les responsabilités.

```text
paylive-ai-copilot/
├── docs/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── src/
│   ├── data_simulation/
│   ├── data_collection/
│   ├── data_processing/
│   └── database/
├── sql/
├── api/
├── tests/
├── diagrams/
└── logs/
```

Cette organisation permet de distinguer :

```text
les données brutes
les extractions intermédiaires
les données nettoyées
les scripts de collecte
les scripts de traitement
les scripts de base de données
l’API REST
les tests
la documentation
les rapports de preuve
```

## 5. Pipeline complet réalisé

Le pipeline final du Bloc 1 est le suivant :

```text
1. Génération de données simulées
2. Analyse qualité des données brutes
3. Collecte depuis fichiers CSV
4. Collecte depuis API externe
5. Collecte depuis scraping autorisé
6. Collecte depuis base SQL simulée
7. Collecte depuis source Big Data Parquet
8. Analyse qualité des données extraites
9. Nettoyage et normalisation
10. Agrégation du dataset final IA
11. Modélisation PostgreSQL
12. Création de la base PostgreSQL
13. Import des données nettoyées
14. Contrôle qualité en base
15. Mise à disposition via API REST
16. Tests automatisés de l’API
17. Documentation RGPD
18. Documentation finale
```

## 6. Résultat final obtenu

À la fin du Bloc 1, le projet dispose de :

```text
scripts de collecte multi-sources
rapports de qualité des données
données nettoyées et normalisées
dataset final agrégé prêt pour l’IA
base PostgreSQL relationnelle
scripts SQL de création
script d’import automatisé
rapports d’import
contrôle qualité en base
API REST FastAPI
documentation Swagger / OpenAPI
sécurité par clé API
tests automatisés
registre RGPD
README d’installation et d’exécution
```

Le dataset final principal est :

```text
data/processed/dataset_final_live_sales.csv
```

La table PostgreSQL correspondante est :

```text
analytics.dataset_final_live_sales
```

Elle contient une ligne par live et des indicateurs agrégés.

## 7. Couverture de la compétence C1

## 7.1. Rappel de l’objectif

La compétence C1 concerne l’automatisation de l’extraction de données depuis plusieurs sources.

Le projet couvre les sources suivantes :

```text
fichiers CSV
API REST externe
page web avec scraping
base de données SQL simulée
source Big Data Parquet
```

## 7.2. Réalisations associées

Les scripts développés sont :

```text
src/data_collection/collect_from_files.py
src/data_collection/collect_from_api.py
src/data_collection/collect_from_scraping.py
src/data_collection/collect_from_database.py
src/data_collection/collect_from_bigdata.py
```

## 7.3. Sources collectées

| Source | Type | Script | Sortie principale |
|---|---|---|---|
| Données simulées | CSV | `collect_from_files.py` | `data/interim/file_extracts/` |
| DummyJSON Products | API REST | `collect_from_api.py` | `data/interim/api_extracts/` |
| Books to Scrape | scraping autorisé | `collect_from_scraping.py` | `data/interim/scraping_extracts/` |
| SQLite legacy | base SQL simulée | `collect_from_database.py` | `data/interim/database_extracts/` |
| Parquet live events | source Big Data | `collect_from_bigdata.py` | `data/interim/bigdata_extracts/` |

## 7.4. Preuves produites

Les preuves principales sont :

```text
data/interim/file_extraction_manifest.csv
data/interim/api_extraction_manifest.csv
data/interim/scraping_extraction_manifest.csv
data/interim/database_extraction_manifest.csv
data/interim/bigdata_extraction_manifest.csv
sql/04_extraction_queries.sql
sql/05_bigdata_extraction_queries.sql
logs/
```

## 7.5. Conclusion C1

La compétence C1 est couverte car le projet automatise l’extraction depuis plusieurs sources hétérogènes et sauvegarde les résultats de manière structurée avec des rapports de suivi.

## 8. Couverture de la compétence C2

## 8.1. Rappel de l’objectif

La compétence C2 concerne le développement de requêtes SQL d’extraction depuis une base de données et un système big data.

## 8.2. Réalisations associées

Deux types de requêtes ont été produits :

```text
requêtes SQL sur une base SQLite simulée
requêtes Spark SQL sur une source Big Data Parquet
```

Fichiers concernés :

```text
sql/04_extraction_queries.sql
sql/05_bigdata_extraction_queries.sql
src/data_collection/collect_from_database.py
src/data_collection/collect_from_bigdata.py
```

## 8.3. Requêtes SQL réalisées

Les requêtes permettent notamment de récupérer :

```text
les vendeurs actifs
les sessions live
les produits associés aux lives
les commentaires exploitables
les commandes et paiements
les événements live agrégés
```

## 8.4. Documentation associée

Les documents associés sont :

```text
docs/09_collecte_depuis_base_donnees.md
docs/10_collecte_depuis_bigdata.md
```

Ils expliquent :

```text
les sources utilisées
les objectifs des requêtes
les choix de sélection
les filtres appliqués
les sorties générées
les contraintes techniques rencontrées
```

## 8.5. Conclusion C2

La compétence C2 est couverte car le projet contient des requêtes SQL et Spark SQL fonctionnelles, documentées et utilisées dans le processus d’extraction.

## 9. Couverture de la compétence C3

## 9.1. Rappel de l’objectif

La compétence C3 concerne l’agrégation des données, la suppression des entrées corrompues et l’homogénéisation des formats.

## 9.2. Réalisations associées

Les scripts principaux sont :

```text
src/data_processing/analyze_raw_data_quality.py
src/data_processing/analyze_extracted_data_quality.py
src/data_processing/clean_and_standardize_data.py
src/data_processing/build_final_ai_dataset.py
```

## 9.3. Contrôles qualité réalisés

Les contrôles réalisés portent sur :

```text
présence des fichiers attendus
présence des colonnes attendues
valeurs manquantes
doublons
emails invalides
dates invalides
statuts non autorisés
montants négatifs
relations invalides
incohérences temporelles
incohérences financières
```

## 9.4. Nettoyages réalisés

Les traitements de nettoyage incluent :

```text
suppression ou correction des doublons
normalisation des plateformes
normalisation des statuts
normalisation des dates
normalisation des devises
correction des montants
recalcul des totaux
contrôle des clés étrangères
standardisation des valeurs textuelles
exclusion des lignes non exploitables
```

## 9.5. Agrégation finale

Le dataset final :

```text
data/processed/dataset_final_live_sales.csv
```

agrège les données au niveau d’un live.

Il combine notamment :

```text
live_sessions
sellers
live_comments
carts
orders
payments
live_products
products
live_events
```

## 9.6. Indicateurs produits

Le dataset final contient des indicateurs comme :

```text
total_comments
purchase_intent_comments
total_carts
paid_carts
abandoned_carts
total_orders
total_revenue
average_order_amount
payment_success_rate
conversion_rate
top_product_category
peak_viewers
api_error_events
final_dataset_status
```

## 9.7. Preuves produites

Les preuves principales sont :

```text
data/interim/quality_report_files.csv
data/interim/quality_report_columns.csv
data/interim/quality_report_business_rules.csv
data/interim/extracted_quality_file_report.csv
data/interim/extracted_quality_column_report.csv
data/interim/extracted_quality_business_rules_report.csv
data/processed/cleaning_summary.csv
data/processed/cleaning_operations_report.csv
data/processed/final_dataset_manifest.csv
data/processed/final_dataset_quality_report.csv
data/processed/final_dataset_aggregation_report.csv
```

## 9.8. Conclusion C3

La compétence C3 est couverte car les données issues de plusieurs sources sont nettoyées, normalisées, contrôlées puis agrégées dans un dataset final exploitable pour la suite IA.

## 10. Couverture de la compétence C4

## 10.1. Rappel de l’objectif

La compétence C4 concerne la création d’une base de données, la modélisation, l’import des données et la prise en compte du RGPD.

## 10.2. Modélisation réalisée

La base PostgreSQL a été organisée en trois schémas :

```text
core
analytics
audit
```

Le schéma `core` contient les données métier détaillées.

Le schéma `analytics` contient le dataset final agrégé.

Le schéma `audit` contient les traces d’import.

## 10.3. Tables principales créées

Tables du schéma `core` :

```text
sellers
customers
products
live_sessions
live_products
live_comments
carts
cart_items
orders
payments
stock_movements
live_events
```

Table du schéma `analytics` :

```text
dataset_final_live_sales
```

Tables du schéma `audit` :

```text
import_batches
import_logs
```

## 10.4. Scripts SQL produits

Les scripts SQL sont :

```text
sql/01_create_database.sql
sql/02_create_schemas.sql
sql/03_create_tables.sql
sql/04_create_indexes.sql
```

## 10.5. Import automatisé

Le script d’import est :

```text
src/database/import_processed_data.py
```

Il permet d’importer les fichiers nettoyés et le dataset final dans PostgreSQL.

Il produit :

```text
data/processed/database_import_report.csv
data/processed/database_import_summary.csv
logs/import_processed_data.log
```

## 10.6. Contrôle qualité en base

Le contrôle qualité en base est réalisé par :

```text
src/database/check_database_quality.py
```

Il vérifie notamment :

```text
existence des tables
nombre de lignes
clés primaires
doublons
relations entre tables
valeurs autorisées
cohérence du dataset final
statut du dernier import
```

Rapports produits :

```text
data/processed/database_quality_table_report.csv
data/processed/database_quality_relationship_report.csv
data/processed/database_quality_business_report.csv
data/processed/database_quality_summary.csv
```

## 10.7. Prise en compte RGPD

Le projet applique une démarche RGPD adaptée au contexte académique.

Les mesures principales sont :

```text
aucune donnée réelle PayLive
données fictives et simulées
absence de données bancaires réelles
pseudonymisation par identifiants techniques
séparation core / analytics / audit
dataset final agrégé par live
non-exposition des emails et téléphones via l’API
documentation du registre RGPD
procédures de tri et de conformité
```

Document associé :

```text
docs/19_registre_rgpd.md
```

## 10.8. Conclusion C4

La compétence C4 est couverte car la base PostgreSQL est modélisée, créée, alimentée par script, contrôlée et documentée avec une prise en compte du RGPD.

## 11. Couverture de la compétence C5

## 11.1. Rappel de l’objectif

La compétence C5 concerne la mise à disposition du jeu de données via une API REST.

## 11.2. API développée

L’API a été développée avec :

```text
FastAPI
Uvicorn
Pydantic
psycopg2-binary
python-dotenv
Swagger / OpenAPI
```

Structure principale :

```text
api/
├── main.py
├── database.py
├── security.py
├── schemas.py
└── routes/
    ├── health.py
    ├── lives.py
    ├── sellers.py
    └── analytics.py
```

## 11.3. Routes publiques

```text
GET /
GET /health
GET /openapi.json
```

## 11.4. Routes protégées

```text
GET /api/v1/sellers
GET /api/v1/sellers/{seller_id}/lives
GET /api/v1/sellers/summary/performance
GET /api/v1/lives
GET /api/v1/lives/{live_id}
GET /api/v1/analytics/top-lives
GET /api/v1/analytics/platform-summary
GET /api/v1/analytics/conversion-insights
```

## 11.5. Sécurité API

Les routes métier sont protégées par le header :

```text
X-API-Key
```

Comportements validés :

```text
clé absente -> 401 Unauthorized
clé invalide -> 403 Forbidden
clé valide -> accès autorisé
```

## 11.6. Documentation API

La documentation Swagger est disponible à l’adresse :

```text
http://127.0.0.1:8000/docs
```

Le schéma OpenAPI est disponible à l’adresse :

```text
http://127.0.0.1:8000/openapi.json
```

Document associé :

```text
docs/18_api_rest_mise_a_disposition_donnees.md
```

## 11.7. Tests automatisés

Les tests automatisés sont dans :

```text
tests/test_api.py
```

Commande exécutée :

```bash
pytest tests/test_api.py -v
```

Résultat obtenu :

```text
14 passed
0 failed
```

Rapport généré :

```text
data/processed/api_test_report.csv
```

## 11.8. Conclusion C5

La compétence C5 est couverte car le dataset est exposé via une API REST fonctionnelle, documentée avec OpenAPI, sécurisée par clé API et validée par des tests automatisés.

## 12. Tableau de synthèse C1 à C5

| Compétence | Attendu principal | Réalisation dans le projet | Preuves |
|---|---|---|---|
| C1 | Automatiser l’extraction multi-sources | CSV, API REST, scraping, SQL, Big Data Parquet | scripts `src/data_collection/`, manifests, logs |
| C2 | Développer des requêtes SQL | SQL SQLite et Spark SQL | `sql/04_extraction_queries.sql`, `sql/05_bigdata_extraction_queries.sql` |
| C3 | Nettoyer, normaliser, agréger | Qualité, nettoyage, dataset final IA | scripts `src/data_processing/`, rapports qualité |
| C4 | Créer la base, importer, RGPD | PostgreSQL, schémas, tables, import, registre RGPD | scripts SQL, import report, database quality, registre RGPD |
| C5 | Développer une API REST | FastAPI, Swagger, API key, routes testées | `api/`, Swagger, OpenAPI, `tests/test_api.py` |

## 13. Documents produits pour le Bloc 1

Les documents principaux sont :

```text
docs/00_contexte_projet.md
docs/01_specifications_techniques_bloc1.md
docs/02_sources_donnees.md
docs/03_dictionnaire_donnees.md
docs/05_analyse_qualite_donnees_brutes.md
docs/06_collecte_depuis_fichiers.md
docs/07_collecte_depuis_api.md
docs/08_collecte_depuis_scraping.md
docs/09_collecte_depuis_base_donnees.md
docs/10_collecte_depuis_bigdata.md
docs/12_nettoyage_normalisation_donnees.md
docs/13_aggregation_dataset_final_ia.md
docs/14_modelisation_base_donnees.md
docs/15_creation_base_donnees_postgresql.md
docs/16_import_donnees_postgresql.md
docs/17_controle_qualite_base_donnees.md
docs/18_api_rest_mise_a_disposition_donnees.md
docs/19_registre_rgpd.md
docs/20_bilan_bloc1.md
README.md
```

## 14. Rapports de preuve produits

Les rapports principaux sont :

```text
data/interim/quality_report_files.csv
data/interim/quality_report_columns.csv
data/interim/quality_report_business_rules.csv
data/interim/extracted_quality_file_report.csv
data/interim/extracted_quality_column_report.csv
data/interim/extracted_quality_business_rules_report.csv
data/processed/cleaning_summary.csv
data/processed/cleaning_operations_report.csv
data/processed/processed_manifest.csv
data/processed/final_dataset_manifest.csv
data/processed/final_dataset_quality_report.csv
data/processed/final_dataset_aggregation_report.csv
data/processed/database_import_report.csv
data/processed/database_import_summary.csv
data/processed/database_quality_table_report.csv
data/processed/database_quality_relationship_report.csv
data/processed/database_quality_business_report.csv
data/processed/database_quality_summary.csv
data/processed/api_test_report.csv
```

## 15. Difficultés rencontrées

## 15.1. Problème PySpark sous Windows

Lors de la collecte Big Data, plusieurs erreurs liées à l’environnement Windows et à PySpark ont été rencontrées.

Exemples :

```text
HADOOP_HOME and hadoop.home.dir are unset
Python worker failed to connect back
winutils.exe warning
```

La solution retenue a été :

```text
utilisation de PyArrow pour créer le Parquet
lecture contrôlée du Parquet
configuration explicite de l’exécutable Python
réduction du contexte Spark en local[1]
maintien d’une extraction Big Data fonctionnelle et documentée
```

## 15.2. Problème d’import PostgreSQL du dataset final

Pendant l’import, PostgreSQL a refusé certaines colonnes entières contenant des valeurs au format décimal.

Erreur rencontrée :

```text
invalid input syntax for type integer: "3.0"
```

Cause :

```text
Pandas avait converti certaines colonnes de comptage en float pendant les jointures.
```

Correction :

```text
conversion explicite des colonnes de comptage en integer dans build_final_ai_dataset.py
régénération du dataset final
réimport PostgreSQL
contrôle qualité base
test API
```

## 15.3. Problème de test Swagger sans clé API

Lors des premiers tests API, les routes protégées retournaient :

```text
Missing API key
```

Cause :

```text
la route était appelée directement depuis le navigateur sans header X-API-Key
```

Correction :

```text
utilisation du bouton Authorize dans Swagger
test avec header X-API-Key
test PowerShell
tests automatisés pytest
```

## 16. Contrôles finaux réalisés

Les contrôles finaux effectués sont :

```text
génération des données brutes
analyse qualité des données brutes
collecte multi-sources
analyse qualité des données extraites
nettoyage et normalisation
génération du dataset final
création PostgreSQL
import des données
contrôle qualité en base
tests manuels Swagger
tests automatisés Pytest
vérification de la documentation
vérification du registre RGPD
```

## 17. Commandes de vérification finale

Les commandes principales sont :

```bash
python src/data_processing/clean_and_standardize_data.py
python src/data_processing/build_final_ai_dataset.py
python src/database/import_processed_data.py
python src/database/check_database_quality.py
pytest tests/test_api.py -v
```

Lancement de l’API :

```bash
python -m uvicorn api.main:app --reload
```

Accès Swagger :

```text
http://127.0.0.1:8000/docs
```

## 18. État final du Bloc 1

L’état final du Bloc 1 est le suivant :

| Élément | Statut |
|---|---|
| Données simulées générées | terminé |
| Collecte fichiers | terminé |
| Collecte API | terminé |
| Collecte scraping | terminé |
| Collecte SQL | terminé |
| Collecte Big Data | terminé |
| Qualité données brutes | terminé |
| Qualité données extraites | terminé |
| Nettoyage et normalisation | terminé |
| Dataset final IA | terminé |
| Modélisation PostgreSQL | terminé |
| Création base PostgreSQL | terminé |
| Import PostgreSQL | terminé |
| Contrôle qualité base | terminé |
| API REST | terminé |
| Sécurité API | terminé |
| Swagger / OpenAPI | terminé |
| Tests automatisés API | terminé |
| Registre RGPD | terminé |
| README global | terminé |
| Bilan Bloc 1 | terminé |

## 19. Limites du Bloc 1

Certaines limites sont assumées :

```text
données uniquement simulées
API exécutée localement
authentification simple par clé API
pas encore de déploiement cloud
pas encore de monitoring applicatif avancé
pas encore de tableau de bord utilisateur
pas encore de modèle IA entraîné dans ce bloc
```

Ces limites sont cohérentes avec le périmètre du Bloc 1.

Elles pourront être traitées dans les blocs suivants.

## 20. Préparation du Bloc 2

Le Bloc 1 prépare directement la suite IA.

Les éléments réutilisables pour le Bloc 2 sont :

```text
dataset final agrégé
commentaires nettoyés
labels d’intention d’achat
produits normalisés
indicateurs de conversion
API REST
base PostgreSQL
documentation technique
tests
```

Les travaux possibles pour le Bloc 2 sont :

```text
analyse exploratoire des commentaires
préparation d’un dataset NLP
benchmark de modèles de classification
entraînement d’un modèle de détection d’intention
évaluation du modèle
exposition d’un endpoint IA
suivi des performances du modèle
```

## 21. Conclusion finale

Le Bloc 1 du projet **PayLive AI Copilot** est finalisé.

Le projet démontre une chaîne complète de traitement de données :

```text
collecte multi-sources
contrôle qualité
nettoyage
normalisation
agrégation
stockage PostgreSQL
import automatisé
contrôle qualité en base
mise à disposition API REST
sécurité par clé API
documentation technique
tests automatisés
prise en compte RGPD
```

Les compétences C1 à C5 sont couvertes par des scripts fonctionnels, des documents techniques, des rapports de preuve et une API testée.

Le socle de données est maintenant prêt pour la suite du projet, notamment l’intégration de fonctionnalités d’intelligence artificielle dans le Bloc 2.