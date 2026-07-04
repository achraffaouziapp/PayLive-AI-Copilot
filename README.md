# PayLive-AI-Copilot

## 1. Présentation du projet

**PayLive AI Copilot** est un projet de dossier professionnel réalisé dans le cadre du titre **Développeur en intelligence artificielle**.

Le projet consiste à construire un socle de données pour un assistant intelligent destiné aux vendeurs qui réalisent des ventes en live sur des plateformes comme TikTok Live ou Instagram Live.

L’objectif métier est d’aider un vendeur à :

```text
détecter les intentions d’achat dans les commentaires
suivre les paniers et les commandes
analyser la performance commerciale des lives
préparer des données exploitables pour de futures fonctionnalités IA
exposer les indicateurs via une API REST
```

Le Bloc 1 porte sur la collecte, le nettoyage, le stockage et la mise à disposition des données.

## 2. Important — Données utilisées

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
```

Les anomalies volontairement présentes dans les données permettent de démontrer les étapes de contrôle qualité, nettoyage et normalisation.

## 3. Fonctionnalités couvertes dans le Bloc 1

Le Bloc 1 couvre les étapes suivantes :

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
tests automatisés de l’API
prise en compte RGPD
```

## 4. Architecture du projet

```text
paylive-ai-copilot/
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── requirements.txt
├── docs/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── bigdata/
├── notebooks/
├── src/
│   ├── config/
│   ├── data_collection/
│   ├── data_simulation/
│   ├── data_processing/
│   ├── database/
│   └── utils/
├── sql/
├── api/
│   ├── main.py
│   ├── database.py
│   ├── security.py
│   ├── schemas.py
│   └── routes/
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

Créer un fichier `.env` à partir du fichier `.env.example`.

Exemple de configuration locale :

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=paylive_ai_copilot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

API_KEY=paylive-dev-api-key
```

Le fichier `.env` ne doit pas être versionné dans Git.

Le fichier `.env.example` sert uniquement de modèle.

## 8. Lancement de PostgreSQL et pgAdmin

Démarrer les conteneurs Docker :

```bash
docker compose up -d
```

Vérifier que les conteneurs sont actifs :

```bash
docker ps
```

Conteneurs attendus :

```text
paylive_postgres
paylive_pgadmin
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

## 9. Ordre d’exécution du pipeline Bloc 1

### 9.1. Génération des données simulées

```bash
python src/data_simulation/generate_raw_data.py
```

Cette étape génère les fichiers bruts dans :

```text
data/raw/
```

### 9.2. Analyse qualité des données brutes

```bash
python src/data_processing/analyze_raw_data_quality.py
```

Rapports générés :

```text
data/interim/quality_report_files.csv
data/interim/quality_report_columns.csv
data/interim/quality_report_business_rules.csv
```

### 9.3. Collecte depuis fichiers CSV

```bash
python src/data_collection/collect_from_files.py
```

### 9.4. Collecte depuis API externe

```bash
python src/data_collection/collect_from_api.py
```

### 9.5. Collecte depuis scraping autorisé

```bash
python src/data_collection/collect_from_scraping.py
```

### 9.6. Collecte depuis base SQL simulée

```bash
python src/data_collection/collect_from_database.py
```

### 9.7. Collecte depuis source Big Data Parquet

```bash
python src/data_collection/collect_from_bigdata.py
```

### 9.8. Analyse qualité des données extraites

```bash
python src/data_processing/analyze_extracted_data_quality.py
```

### 9.9. Nettoyage et normalisation

```bash
python src/data_processing/clean_and_standardize_data.py
```

Fichiers générés :

```text
data/processed/*_clean.csv
data/processed/cleaning_summary.csv
data/processed/cleaning_operations_report.csv
```

### 9.10. Construction du dataset final IA

```bash
python src/data_processing/build_final_ai_dataset.py
```

Fichier principal généré :

```text
data/processed/dataset_final_live_sales.csv
```

## 10. Création de la base PostgreSQL

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

## 11. Import des données dans PostgreSQL

Importer les fichiers nettoyés et le dataset final :

```bash
python src/database/import_processed_data.py
```

Rapports générés :

```text
data/processed/database_import_report.csv
data/processed/database_import_summary.csv
```

Vérifier le nombre de lignes du dataset final :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "SELECT COUNT(*) FROM analytics.dataset_final_live_sales;"
```

## 12. Contrôle qualité de la base

```bash
python src/database/check_database_quality.py
```

Rapports générés :

```text
data/processed/database_quality_table_report.csv
data/processed/database_quality_relationship_report.csv
data/processed/database_quality_business_report.csv
data/processed/database_quality_summary.csv
```

## 13. Lancement de l’API REST

Lancer l’API FastAPI :

```bash
python -m uvicorn api.main:app --reload
```

L’API est disponible ici :

```text
http://127.0.0.1:8000
```

Documentation Swagger :

```text
http://127.0.0.1:8000/docs
```

Schéma OpenAPI :

```text
http://127.0.0.1:8000/openapi.json
```

## 14. Sécurité de l’API

Les routes métier sont protégées par clé API.

Header obligatoire :

```text
X-API-Key: paylive-dev-api-key
```

Si la clé API est absente, l’API retourne :

```text
401 Unauthorized
```

Si la clé API est invalide, l’API retourne :

```text
403 Forbidden
```

## 15. Routes principales de l’API

Routes publiques :

```text
GET /
GET /health
GET /openapi.json
```

Routes protégées :

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

## 16. Exemple de test API avec PowerShell

```powershell
$headers = @{ "X-API-Key" = "paylive-dev-api-key" }

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/sellers?limit=5&offset=0" `
  -Headers $headers
```

## 17. Tests automatisés

Les tests automatisés de l’API sont dans :

```text
tests/test_api.py
```

Exécuter les tests :

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

Les tests vérifient notamment :

```text
route publique /
route publique /health
documentation OpenAPI
accès refusé sans clé API
accès refusé avec clé API invalide
accès accepté avec clé API valide
routes sellers
routes lives
routes analytics
connexion PostgreSQL
```

## 18. Documentation du projet

Les principaux documents du Bloc 1 sont :

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
```

## 19. Rapports générés

Les principaux rapports de preuve sont :

```text
data/interim/quality_report_files.csv
data/interim/quality_report_columns.csv
data/interim/quality_report_business_rules.csv
data/interim/extracted_quality_file_report.csv
data/interim/extracted_quality_column_report.csv
data/interim/extracted_quality_business_rules_report.csv
data/processed/cleaning_summary.csv
data/processed/cleaning_operations_report.csv
data/processed/final_dataset_quality_report.csv
data/processed/database_import_report.csv
data/processed/database_import_summary.csv
data/processed/database_quality_summary.csv
data/processed/api_test_report.csv
```

## 20. Prise en compte RGPD

Le projet prend en compte le RGPD par :

```text
l’utilisation de données fictives
l’absence de données PayLive réelles
l’absence de données bancaires réelles
la pseudonymisation des identifiants
la séparation des schémas core, analytics et audit
l’agrégation du dataset final par live
la non-exposition des emails, téléphones et commentaires bruts via l’API
la protection des routes API par clé API
la documentation des traitements dans le registre RGPD
```

Le document de référence est :

```text
docs/19_registre_rgpd.md
```

## 21. Fichiers à ne pas versionner

Le fichier `.env` ne doit pas être versionné.

Exemple de règles `.gitignore` recommandées :

```gitignore
.env
.venv/
__pycache__/
*.pyc
logs/*.log
data/raw/scraping_html/
data/raw/bigdata/
data/raw/legacy_database/
.pytest_cache/
```

Certains fichiers de données peuvent être conservés temporairement comme preuves pour le dossier, selon les besoins de l’évaluation.

## 22. Résultat final du Bloc 1

À la fin du Bloc 1, le projet dispose :

```text
d’un pipeline de collecte multi-sources
de données brutes, intermédiaires et nettoyées
d’un dataset final agrégé prêt pour l’IA
d’une base PostgreSQL relationnelle
d’un import automatisé
d’un contrôle qualité en base
d’une API REST sécurisée
d’une documentation Swagger / OpenAPI
de tests automatisés
d’un registre RGPD
d’une documentation technique complète
```

## 23. Commande complète de vérification finale

Une fois PostgreSQL lancé, les principales commandes de vérification sont :

```bash
python src/data_processing/clean_and_standardize_data.py
python src/data_processing/build_final_ai_dataset.py
python src/database/import_processed_data.py
python src/database/check_database_quality.py
pytest tests/test_api.py -v
```

Puis lancer l’API :

```bash
python -m uvicorn api.main:app --reload
```

## 24. Conclusion

Le projet **PayLive AI Copilot** met en place une chaîne complète de traitement de données pour un contexte de live shopping.

Le Bloc 1 permet de démontrer la capacité à collecter des données multi-sources, les nettoyer, les agréger, les stocker dans PostgreSQL et les exposer via une API REST sécurisée.

Ce socle technique prépare les étapes suivantes du projet, notamment le développement de fonctionnalités d’intelligence artificielle pour la détection d’intention d’achat et l’aide à la décision commerciale.