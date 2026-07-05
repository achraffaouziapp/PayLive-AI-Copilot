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
intégrer le service IA dans une application web
monitorer le service IA
suivre les alertes et les métriques du modèle
```

Le projet couvre trois blocs :

```text
Bloc 1 — Collecte, préparation, stockage et mise à disposition des données
Bloc 2 — Intégration d’un service IA, API, tests, monitoring et MLOps
Bloc 3 — Application web HTML/CSS/JS conteneurisée intégrant le service IA
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

### 3.3. Bloc 3 — Application web

Le Bloc 3 couvre :

```text
analyse du besoin applicatif
spécifications fonctionnelles et user stories
critères d’acceptation
architecture applicative
parcours utilisateurs
objectifs d’accessibilité
développement d’une interface HTML/CSS/JavaScript
intégration de l’API IA
conteneurisation Docker/Nginx
sécurisation des appels par X-API-Key
tests frontend statiques
intégration des tests frontend dans GitHub Actions
pilotage avec Jira
documentation des incidents et de la maintenance
```

L’application web permet de :

```text
saisir un commentaire de live
tester la clé API sur une route protégée
envoyer un commentaire au modèle IA
afficher l’intention prédite
afficher le score de confiance
afficher une alerte en cas de faible confiance
charger les informations du modèle
charger les métriques du modèle
ouvrir le dashboard monitoring
télécharger les alertes CSV
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
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
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
│   ├── 07_ai_service/
│   └── 08_application/
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
un compte Jira pour le suivi des tâches Bloc 3
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

Côté frontend :

```text
HTML
CSS
JavaScript natif
Nginx
Docker
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
docker compose up -d --build
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
paylive_frontend
```

Accès frontend :

```text
http://127.0.0.1:8080
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

## 12. Application Bloc 3 — Frontend HTML/CSS/JS

Le frontend est situé dans :

```text
frontend/
```

Il est servi par Nginx et exposé sur :

```text
http://127.0.0.1:8080
```

### 12.1. Fonctions disponibles dans l’interface

L’interface permet de :

```text
tester la connexion sécurisée à l’API IA
saisir un commentaire de live
appeler le modèle IA
afficher l’intention prédite
afficher le score de confiance
afficher le temps de réponse
afficher la version du modèle
afficher une alerte de faible confiance
charger les informations modèle
charger les métriques modèle
ouvrir le dashboard de monitoring
télécharger les alertes CSV
```

### 12.2. Proxy Nginx

Le fichier :

```text
frontend/nginx.conf
```

sert l’application et proxifie :

```text
/health → http://api:8000/health
/api/   → http://api:8000/api/
```

Cela permet au JavaScript d’utiliser des URLs relatives :

```text
/health
/api/v1/ai
```

### 12.3. Commandes frontend

Construire uniquement le frontend :

```bash
docker compose build frontend
```

Lancer le frontend :

```bash
docker compose up -d frontend
```

Consulter les logs :

```bash
docker logs --tail 80 paylive_frontend
```

Tester le frontend :

```bash
curl http://127.0.0.1:8080
```

## 13. API REST

L’API est développée avec FastAPI.

Lancement local :

```bash
python -m uvicorn api.main:app --reload
```

Lancement Docker :

```bash
docker compose up -d --build
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

## 14. Sécurité API

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

Dans le frontend, le bouton de test de connexion vérifie une route protégée afin de valider réellement la clé API.

## 15. Routes principales

### 15.1. Routes publiques

```text
GET /
GET /health
GET /openapi.json
```

### 15.2. Routes métier Bloc 1

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

### 15.3. Routes IA Bloc 2 et utilisées par le Bloc 3

```text
POST /api/v1/ai/predict-intent
POST /api/v1/ai/batch-predict-intents
GET  /api/v1/ai/model-info
GET  /api/v1/ai/model-metrics
GET  /api/v1/ai/monitoring/dashboard
GET  /api/v1/ai/monitoring/alerts
```

## 16. Exemples d’appels API

### 16.1. Test santé

```bash
curl http://127.0.0.1:8000/health
```

### 16.2. Prédiction d’intention

Commande Windows CMD :

```cmd
curl -H "X-API-Key: paylive-dev-api-key" -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/api/v1/ai/predict-intent -d "{\"comment_text\":\"je prends la robe noire en M\"}"
```

### 16.3. Télécharger le dashboard de monitoring IA

```cmd
curl -H "X-API-Key: paylive-dev-api-key" -o dashboard.html http://127.0.0.1:8000/api/v1/ai/monitoring/dashboard
start dashboard.html
```

### 16.4. Télécharger les alertes de monitoring IA

```cmd
curl -H "X-API-Key: paylive-dev-api-key" -o alerts.csv http://127.0.0.1:8000/api/v1/ai/monitoring/alerts
```

## 17. Tests automatisés

### 17.1. Tests Bloc 1

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

### 17.2. Tests Bloc 2

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

### 17.3. Tests Bloc 3

```bash
pytest tests/test_frontend_static.py -v
```

Tests couverts :

```text
présence des fichiers frontend
présence des sections principales dans index.html
présence des routes API dans app.js
présence du header X-API-Key
validation de la clé API sur une route protégée
règles CSS responsive
configuration Nginx
Dockerfile frontend
```

### 17.4. Test complet

```bash
pytest tests/test_api.py tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py tests/test_frontend_static.py -v
```

## 18. Pipeline MLOps et CI/CD GitHub Actions

Un workflow GitHub Actions automatise la chaîne IA et application.

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
tests frontend statiques
build Docker du frontend
publication des rapports en artefacts
```

Le pipeline passe en vert sur GitHub Actions.

## 19. Pilotage avec Jira

Le suivi du Bloc 3 est documenté dans :

```text
docs/08_application/39_pilotage_jira_bloc3.md
```

Jira est utilisé pour suivre :

```text
les user stories
les tâches techniques
les bugs
les corrections
les critères d’acceptation
l’état d’avancement
les preuves de réalisation
```

Types de tickets utilisés :

```text
Epic
Story
Task
Bug
Improvement
```

## 20. Documentation du projet

### 20.1. Documentation Bloc 1

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

### 20.2. Documentation Bloc 2

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

### 20.3. Documentation Bloc 3

```text
docs/08_application/31_cadrage_application_bloc3.md
docs/08_application/32_specifications_fonctionnelles.md
docs/08_application/33_architecture_application.md
docs/08_application/34_user_stories_accessibilite.md
docs/08_application/35_developpement_interface.md
docs/08_application/36_tests_application.md
docs/08_application/37_bilan_bloc3.md
docs/08_application/38_checklist_captures_bloc3.md
docs/08_application/39_pilotage_jira_bloc3.md
docs/08_application/40_incidents_maintenance_bloc3.md
```

## 21. Rapports générés

### 21.1. Rapports Bloc 1

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

### 21.2. Rapports Bloc 2

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

### 21.3. Preuves Bloc 3

```text
frontend/
tests/test_frontend_static.py
.github/workflows/ai_mlops_ci.yml
docs/08_application/
captures d’écran Jira
captures d’écran frontend
captures d’écran prédiction IA
captures d’écran dashboard monitoring
captures d’écran GitHub Actions
captures d’écran Docker Compose
```

## 22. RGPD, sécurité et OWASP

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

Mesures de sécurité appliquées :

```text
routes protégées par X-API-Key
validation des entrées côté API
gestion des erreurs 401 et 403
proxy Nginx vers l’API Docker
absence d’appel à un fournisseur IA externe
absence de données réelles
logs Docker consultables
monitoring IA avec dashboard et alertes
documentation des incidents et procédures de maintenance
```

## 23. Incidents et maintenance

Les incidents et corrections du Bloc 3 sont documentés dans :

```text
docs/08_application/40_incidents_maintenance_bloc3.md
```

Exemples d’incidents corrigés :

```text
mise en page JSON trop large dans le frontend
sections informations modèle et métriques modèle affichées sur la même ligne
test de clé API basé sur /health alors que /health est public
correction du test de clé API sur une route protégée
```

Commandes utiles de diagnostic :

```bash
docker compose ps
docker logs --tail 80 paylive_frontend
docker logs --tail 80 paylive_api
curl http://127.0.0.1:8080
curl http://127.0.0.1:8000/health
pytest tests/test_frontend_static.py -v
```

## 24. Fichiers à ne pas versionner

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

## 25. Commandes de vérification finale

### 25.1. Vérification Bloc 1

```bash
python src/data_processing/clean_and_standardize_data.py
python src/data_processing/build_final_ai_dataset.py
python src/database/import_processed_data.py
python src/database/check_database_quality.py
pytest tests/test_api.py -v
```

### 25.2. Vérification Bloc 2

```bash
python src/ai/data_preparation/prepare_nlp_dataset.py
python src/ai/training/train_intent_classifier.py
python src/ai/training/benchmark_intent_models.py
python src/ai/monitoring/monitor_predictions.py
python src/ai/monitoring/generate_monitoring_dashboard.py
pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py -v
```

### 25.3. Vérification Bloc 3

```bash
docker compose up -d --build
pytest tests/test_frontend_static.py -v
curl http://127.0.0.1:8080
curl http://127.0.0.1:8000/health
```

### 25.4. Vérification complète

```bash
pytest tests/test_api.py tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py tests/test_frontend_static.py -v
```

### 25.5. Vérification Docker complète

```bash
docker compose up -d --build
docker compose ps
```

Vérifier ensuite :

```text
http://127.0.0.1:8080
http://127.0.0.1:8000/docs
http://127.0.0.1:5050
```

## 26. Résultat final

À la fin des trois blocs, le projet dispose :

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
de tests automatisés Bloc 1, Bloc 2 et Bloc 3
d’un monitoring IA
d’un dashboard HTML
d’alertes CSV
d’un frontend HTML/CSS/JavaScript
d’un frontend conteneurisé avec Docker et Nginx
d’une intégration frontend → API IA
d’un suivi Jira du Bloc 3
d’une documentation des incidents et de la maintenance
d’un pipeline CI/CD GitHub Actions
d’une documentation technique complète
```

## 27. Conclusion

Le projet **PayLive AI Copilot** met en place une chaîne complète allant de la collecte des données jusqu’à l’intégration d’un service IA dans une application web.

Le Bloc 1 démontre la capacité à collecter, nettoyer, structurer, stocker et exposer des données via une API REST sécurisée.

Le Bloc 2 démontre la capacité à réaliser une veille IA, benchmarker des solutions, entraîner un modèle, l’exposer via API, le tester, le monitorer et l’intégrer dans une chaîne MLOps légère.

Le Bloc 3 démontre la capacité à analyser un besoin applicatif, spécifier des user stories, concevoir une architecture technique, développer une interface web, intégrer un service IA, sécuriser les accès, tester l’application, suivre les tâches avec Jira et automatiser la validation dans une chaîne CI/CD.

La solution finale reste volontairement locale, explicable, sobre et conteneurisée, ce qui correspond au contexte pédagogique, aux contraintes du projet et aux attendus du dossier professionnel.
