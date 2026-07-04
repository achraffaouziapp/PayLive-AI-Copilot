# PayLive AI Copilot

## 1. Présentation du projet

**PayLive AI Copilot** est un projet de dossier professionnel réalisé dans le cadre du titre **Développeur en intelligence artificielle**.

Le projet consiste à construire un assistant intelligent pour les vendeurs qui réalisent des ventes en live sur des plateformes comme TikTok Live ou Instagram Live.

L’objectif métier est d’aider un vendeur à :

```text
détecter les intentions d’achat dans les commentaires
suivre les paniers et les commandes
analyser la performance commerciale des lives
préparer des données exploitables pour des fonctionnalités IA
exposer les données et les prédictions via une API REST
monitorer le service IA
```

Le projet couvre deux blocs :

```text
Bloc 1 — Collecte, préparation, stockage et mise à disposition des données
Bloc 2 — Intégration d’un service IA, API, tests, monitoring et MLOps
```

## 2. Données utilisées

Le projet n’utilise aucune donnée réelle de l’entreprise PayLive.

Les données sont :

```text
simulées
fictives
pseudonymisées
générées artificiellement
issues de sources externes autorisées pour l’entraînement
```

Le projet ne contient pas :

```text
données PayLive réelles
données bancaires réelles
numéros de carte bancaire
IBAN
documents d’identité
mots de passe utilisateurs
adresses personnelles réelles
```

Les anomalies volontairement présentes dans les données permettent de démontrer les étapes de contrôle qualité, nettoyage, normalisation, monitoring et test.

## 3. Fonctionnalités principales

### 3.1. Bloc 1 — Données et API métier

Le Bloc 1 couvre :

```text
collecte multi-sources
extraction depuis fichiers CSV
extraction depuis API externe
extraction depuis scraping autorisé
extraction depuis base SQL simulée
extraction depuis source Big Data Parquet
analyse qualité des données
nettoyage et normalisation
agrégation du dataset final IA
modélisation PostgreSQL
création de la base de données
import des données nettoyées
contrôle qualité en base
mise à disposition via API REST FastAPI
sécurisation par clé API
documentation Swagger / OpenAPI
tests automatisés API
prise en compte RGPD
```

### 3.2. Bloc 2 — Service IA

Le Bloc 2 couvre :

```text
veille technique et réglementaire IA
benchmark de modèles et services IA
analyse coût, prérequis et éco-responsabilité
préparation d’un dataset NLP
entraînement d’un modèle de classification d’intention
benchmark expérimental de modèles
sauvegarde des artefacts du modèle
module d’inférence
API REST exposant le modèle IA
authentification par X-API-Key
tests automatisés IA/API
monitoring des prédictions
dashboard HTML de monitoring
alertes CSV
pipeline GitHub Actions MLOps
```

## 4. Architecture du projet

```text
PayLive-AI-Copilot/
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ai_mlops_ci.yml
├── api/
│   ├── main.py
│   ├── database.py
│   ├── security.py
│   ├── schemas.py
│   ├── ai_service.py
│   └── routes/
│       ├── ai.py
│       ├── analytics.py
│       ├── health.py
│       ├── lives.py
│       └── sellers.py
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── bigdata/
│   └── ai/
│       ├── datasets/
│       ├── predictions/
│       └── reports/
├── docs/
│   ├── 00_project_overview/
│   ├── 01_sources_and_collection/
│   ├── 02_quality_and_processing/
│   ├── 03_database/
│   ├── 04_api/
│   ├── 05_rgpd/
│   ├── 06_bilan/
│   └── 07_ai_service/
├── models/
│   └── intent_classifier/
├── notebooks/
├── sql/
├── src/
│   ├── config/
│   ├── data_collection/
│   ├── data_processing/
│   ├── data_simulation/
│   ├── database/
│   ├── utils/
│   └── ai/
│       ├── data_preparation/
│       ├── inference/
│       ├── monitoring/
│       └── training/
├── tests/
├── diagrams/
└── logs/
```

## 5. Prérequis techniques

Le projet nécessite :

```text
Python 3.11 ou supérieur
Docker Desktop
PostgreSQL via Docker
pgAdmin via Docker
Git
GitHub Actions pour la CI MLOps
```

Bibliothèques Python principales :

```text
pandas
numpy
requests
beautifulsoup4
pyarrow
pyspark
fastapi
uvicorn
pydantic
psycopg2-binary
python-dotenv
pytest
httpx
scikit-learn
joblib
```

## 6. Installation du projet

Cloner le dépôt :

```bash
git clone <url-du-repository>
cd PayLive-AI-Copilot
```

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l’environnement virtuel sous Windows :

```bash
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## 7. Configuration de l’environnement

Créer un fichier `.env` à partir de `.env.example`.

Exemple :

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=paylive_ai_copilot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

API_KEY=paylive-dev-api-key
```

Le fichier `.env` ne doit pas être versionné.

## 8. Lancement avec Docker

Démarrer les services :

```bash
docker compose up -d
```

Vérifier les conteneurs :

```bash
docker compose ps
```

Conteneurs attendus :

```text
paylive_postgres
paylive_pgadmin
paylive_api
```

Accès API :

```text
http://127.0.0.1:8000
```

Documentation Swagger :

```text
http://127.0.0.1:8000/docs
```

Accès pgAdmin :

```text
URL: http://localhost:5050
Email: admin@paylive.com
Password: admin123
```

Connexion PostgreSQL dans pgAdmin :

```text
Host: postgres
Port: 5432
Database: postgres
Username: postgres
Password: postgres
```

Depuis la machine hôte, PostgreSQL est accessible sur :

```text
localhost:5433
```

## 9. Pipeline Bloc 1 — Données

### 9.1. Génération des données simulées

```bash
python src/data_simulation/generate_raw_data.py
```

### 9.2. Analyse qualité des données brutes

```bash
python src/data_processing/analyze_raw_data_quality.py
```

### 9.3. Collecte multi-sources

```bash
python src/data_collection/collect_from_files.py
python src/data_collection/collect_from_api.py
python src/data_collection/collect_from_scraping.py
python src/data_collection/collect_from_database.py
python src/data_collection/collect_from_bigdata.py
```

### 9.4. Analyse qualité des données extraites

```bash
python src/data_processing/analyze_extracted_data_quality.py
```

### 9.5. Nettoyage et normalisation

```bash
python src/data_processing/clean_and_standardize_data.py
```

### 9.6. Construction du dataset final IA

```bash
python src/data_processing/build_final_ai_dataset.py
```

Fichier principal généré :

```text
data/processed/final/dataset_final_live_sales.csv
```

## 10. Base PostgreSQL

Créer la base :

```bash
docker cp sql/01_create_database.sql paylive_postgres:/tmp/01_create_database.sql
docker exec -it paylive_postgres psql -U postgres -d postgres -f /tmp/01_create_database.sql
```

Créer les schémas :

```bash
docker cp sql/02_create_schemas.sql paylive_postgres:/tmp/02_create_schemas.sql
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/02_create_schemas.sql
```

Créer les tables :

```bash
docker cp sql/03_create_tables.sql paylive_postgres:/tmp/03_create_tables.sql
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/03_create_tables.sql
```

Créer les indexes :

```bash
docker cp sql/04_create_indexes.sql paylive_postgres:/tmp/04_create_indexes.sql
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/04_create_indexes.sql
```

Importer les données nettoyées :

```bash
python src/database/import_processed_data.py
```

Contrôler la qualité en base :

```bash
python src/database/check_database_quality.py
```

## 11. Pipeline Bloc 2 — IA

### 11.1. Préparation du dataset NLP

```bash
python src/ai/data_preparation/prepare_nlp_dataset.py
```

Fichiers générés :

```text
data/ai/datasets/comments_intent_dataset.csv
data/ai/datasets/train.csv
data/ai/datasets/validation.csv
data/ai/datasets/test.csv
data/ai/reports/nlp_dataset_quality_report.csv
data/ai/reports/train_validation_test_split_report.csv
```

### 11.2. Entraînement du modèle

```bash
python src/ai/training/train_intent_classifier.py
```

Artefacts générés :

```text
models/intent_classifier/model.joblib
models/intent_classifier/vectorizer.joblib
models/intent_classifier/label_encoder.joblib
models/intent_classifier/model_metadata.json
```

Rapports générés :

```text
data/ai/reports/model_training_report.csv
data/ai/reports/model_evaluation_report.csv
data/ai/reports/classification_report.csv
data/ai/reports/confusion_matrix.csv
```

### 11.3. Benchmark des modèles

```bash
python src/ai/training/benchmark_intent_models.py
```

Rapports générés :

```text
data/ai/reports/model_benchmark_report.csv
data/ai/reports/model_benchmark_classification_report.csv
data/ai/reports/model_benchmark_selection_report.csv
```

Modèle retenu :

```text
tfidf_logistic_regression
```

### 11.4. Monitoring des prédictions

```bash
python src/ai/monitoring/monitor_predictions.py
```

Fichiers générés :

```text
data/ai/predictions/ai_predictions_log.csv
data/ai/reports/model_monitoring_report.csv
```

### 11.5. Dashboard et alertes

```bash
python src/ai/monitoring/generate_monitoring_dashboard.py
```

Fichiers générés :

```text
data/ai/reports/model_monitoring_dashboard.html
data/ai/reports/model_monitoring_alerts.csv
```

Ouvrir le dashboard localement sous Windows :

```cmd
start data\ai\reports\model_monitoring_dashboard.html
```

## 12. API REST

L’API est développée avec FastAPI.

Lancement local :

```bash
python -m uvicorn api.main:app --reload
```

Lancement Docker :

```bash
docker compose up -d
```

URL API :

```text
http://127.0.0.1:8000
```

Swagger :

```text
http://127.0.0.1:8000/docs
```

OpenAPI :

```text
http://127.0.0.1:8000/openapi.json
```

## 13. Sécurité API

Les routes métier et IA sont protégées par clé API.

Header obligatoire :

```text
X-API-Key: paylive-dev-api-key
```

Comportement attendu :

```text
clé absente   → 401 Unauthorized
clé invalide  → 403 Forbidden
clé valide    → 200 OK
```

## 14. Routes principales

### 14.1. Routes publiques

```text
GET /
GET /health
GET /openapi.json
```

### 14.2. Routes métier Bloc 1

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

### 14.3. Routes IA Bloc 2

```text
POST /api/v1/ai/predict-intent
POST /api/v1/ai/batch-predict-intents
GET  /api/v1/ai/model-info
GET  /api/v1/ai/model-metrics
GET  /api/v1/ai/monitoring/dashboard
GET  /api/v1/ai/monitoring/alerts
```

## 15. Exemples d’appels API

### 15.1. Test santé

```bash
curl http://127.0.0.1:8000/health
```

### 15.2. Prédiction d’intention

Commande Windows CMD :

```cmd
curl -H "X-API-Key: paylive-dev-api-key" -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/api/v1/ai/predict-intent -d "{\"comment_text\":\"je prends la robe noire en M\"}"
```

### 15.3. Télécharger le dashboard de monitoring IA

```cmd
curl -H "X-API-Key: paylive-dev-api-key" -o dashboard.html http://127.0.0.1:8000/api/v1/ai/monitoring/dashboard
start dashboard.html
```

### 15.4. Télécharger les alertes de monitoring IA

```cmd
curl -H "X-API-Key: paylive-dev-api-key" -o alerts.csv http://127.0.0.1:8000/api/v1/ai/monitoring/alerts
```

## 16. Tests automatisés

### 16.1. Tests Bloc 1

```bash
pytest tests/test_api.py -v
```

Tests couverts :

```text
routes publiques
sécurité API
routes sellers
routes lives
routes analytics
connexion PostgreSQL
documentation OpenAPI
```

### 16.2. Tests Bloc 2

```bash
pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py -v
```

Tests couverts :

```text
dataset IA
fichiers train / validation / test
chargement du modèle
prédiction d’intention
routes API IA
authentification IA
réponses JSON
```

### 16.3. Test complet

```bash
pytest tests/test_api.py tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py -v
```

## 17. Pipeline MLOps GitHub Actions

Un workflow GitHub Actions automatise la chaîne IA.

Fichier :

```text
.github/workflows/ai_mlops_ci.yml
```

Le pipeline s’exécute sur :

```text
push
pull_request
workflow_dispatch
```

Il lance :

```text
préparation du dataset IA
entraînement du modèle
benchmark des modèles
génération du monitoring
génération du dashboard et des alertes
tests automatisés IA/API
publication des rapports en artefacts
```

Le pipeline passe en vert sur GitHub Actions.

## 18. Documentation du projet

### 18.1. Documentation Bloc 1

```text
docs/00_project_overview/00_contexte_projet.md
docs/00_project_overview/01_specifications_techniques_bloc1.md
docs/00_project_overview/02_sources_donnees.md
docs/00_project_overview/03_dictionnaire_donnees.md

docs/01_sources_and_collection/04_generation_donnees_simulees.md
docs/01_sources_and_collection/06_collecte_depuis_fichiers.md
docs/01_sources_and_collection/07_collecte_depuis_api.md
docs/01_sources_and_collection/08_collecte_depuis_scraping.md
docs/01_sources_and_collection/09_collecte_depuis_base_donnees.md
docs/01_sources_and_collection/10_collecte_depuis_bigdata.md

docs/02_quality_and_processing/05_analyse_qualite_donnees_brutes.md
docs/02_quality_and_processing/11_analyse_qualite_donnees_extraites.md
docs/02_quality_and_processing/12_nettoyage_normalisation_donnees.md
docs/02_quality_and_processing/13_aggregation_dataset_final_ia.md

docs/03_database/14_modelisation_base_donnees.md
docs/03_database/15_creation_base_donnees_postgresql.md
docs/03_database/16_import_donnees_postgresql.md
docs/03_database/17_controle_qualite_base_donnees.md

docs/04_api/18_api_rest_mise_a_disposition_donnees.md
docs/05_rgpd/19_registre_rgpd.md
docs/06_bilan/20_bilan_bloc1.md
```

### 18.2. Documentation Bloc 2

```text
docs/07_ai_service/21_cadrage_bloc2_ia.md
docs/07_ai_service/22_specifications_service_ia.md
docs/07_ai_service/23_veille_technique_reglementaire_ia.md
docs/07_ai_service/24_benchmark_modeles_services_ia.md
docs/07_ai_service/25_preparation_dataset_nlp.md
docs/07_ai_service/26_entrainement_evaluation_modele.md
docs/07_ai_service/27_api_service_ia.md
docs/07_ai_service/28_tests_service_ia.md
docs/07_ai_service/29_monitoring_modele_ia.md
docs/07_ai_service/30_bilan_bloc2.md
```

## 19. Rapports générés

### 19.1. Rapports Bloc 1

```text
data/interim/reports/raw_quality/
data/interim/reports/file_collection/
data/interim/reports/api_collection/
data/interim/reports/scraping_collection/
data/interim/reports/database_collection/
data/interim/reports/bigdata_collection/
data/interim/reports/extracted_quality/

data/processed/reports/cleaning/
data/processed/reports/final_dataset/
data/processed/reports/database_import/
data/processed/reports/database_quality/
data/processed/reports/api_tests/
```

### 19.2. Rapports Bloc 2

```text
data/ai/reports/nlp_dataset_quality_report.csv
data/ai/reports/train_validation_test_split_report.csv
data/ai/reports/model_training_report.csv
data/ai/reports/model_evaluation_report.csv
data/ai/reports/classification_report.csv
data/ai/reports/confusion_matrix.csv
data/ai/reports/model_benchmark_report.csv
data/ai/reports/model_benchmark_classification_report.csv
data/ai/reports/model_benchmark_selection_report.csv
data/ai/reports/ai_dataset_test_report.csv
data/ai/reports/intent_model_test_report.csv
data/ai/reports/ai_api_test_report.csv
data/ai/reports/model_monitoring_report.csv
data/ai/reports/model_monitoring_dashboard.html
data/ai/reports/model_monitoring_alerts.csv
```

## 20. RGPD et sécurité

Le projet prend en compte le RGPD par :

```text
utilisation de données fictives
absence de données PayLive réelles
absence de données bancaires réelles
pseudonymisation des identifiants
minimisation des données exposées
protection des routes API par clé API
non-exposition des données sensibles via l’API
documentation des traitements dans le registre RGPD
```

Document principal :

```text
docs/05_rgpd/19_registre_rgpd.md
```

## 21. Fichiers à ne pas versionner

Le fichier `.env` ne doit pas être versionné.

Exemple de règles `.gitignore` :

```gitignore
.env
.venv/
__pycache__/
*.pyc
logs/*.log
.pytest_cache/
data/raw/scraping_html/
data/raw/bigdata/
data/raw/legacy_database/
```

Selon la stratégie du dossier, certains fichiers CSV de preuve peuvent être versionnés temporairement pour l’évaluation.

## 22. Commandes de vérification finale

### 22.1. Vérification Bloc 1

```bash
python src/data_processing/clean_and_standardize_data.py
python src/data_processing/build_final_ai_dataset.py
python src/database/import_processed_data.py
python src/database/check_database_quality.py
pytest tests/test_api.py -v
```

### 22.2. Vérification Bloc 2

```bash
python src/ai/data_preparation/prepare_nlp_dataset.py
python src/ai/training/train_intent_classifier.py
python src/ai/training/benchmark_intent_models.py
python src/ai/monitoring/monitor_predictions.py
python src/ai/monitoring/generate_monitoring_dashboard.py
pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py -v
```

### 22.3. Vérification Docker

```bash
docker compose up -d
curl http://127.0.0.1:8000/health
```

### 22.4. Vérification complète des tests

```bash
pytest tests/test_api.py tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py -v
```

## 23. Résultat final

À la fin des deux blocs, le projet dispose :

```text
d’un pipeline complet de collecte multi-sources
d’un pipeline de nettoyage et de normalisation
d’un dataset final exploitable pour l’IA
d’une base PostgreSQL relationnelle
d’une API REST sécurisée
d’une documentation Swagger / OpenAPI
d’un registre RGPD
d’un service IA de classification d’intention
d’un modèle entraîné localement
d’un benchmark modèles et services IA
d’un module d’inférence
de routes API IA
de tests automatisés Bloc 1 et Bloc 2
d’un monitoring IA
d’un dashboard HTML
d’alertes CSV
d’un pipeline CI MLOps GitHub Actions
d’une documentation technique complète
```

## 24. Conclusion

Le projet **PayLive AI Copilot** met en place une chaîne complète allant de la collecte des données jusqu’à l’intégration d’un service IA monitoré.

Le Bloc 1 démontre la capacité à collecter, nettoyer, structurer, stocker et exposer des données via une API REST sécurisée.

Le Bloc 2 démontre la capacité à réaliser une veille IA, benchmarker des solutions, entraîner un modèle, l’exposer via API, le tester, le monitorer et l’intégrer dans une chaîne MLOps légère.

La solution finale reste volontairement locale, explicable et sobre, ce qui correspond au contexte pédagogique et aux contraintes du projet.
