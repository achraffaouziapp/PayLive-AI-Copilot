# API REST de mise à disposition des données — Bloc 1

## 1. Objectif

Cette étape a pour objectif de mettre à disposition les données préparées du projet **PayLive AI Copilot** via une API REST.

Après les étapes de collecte, nettoyage, agrégation, stockage PostgreSQL et contrôle qualité en base, les données sont maintenant accessibles à travers des endpoints HTTP.

L’API permet de consulter :

- les vendeurs ;
- les lives ;
- le dataset final agrégé ;
- les indicateurs analytiques ;
- les performances par vendeur ;
- les performances par plateforme.

Cette API constitue la dernière étape de mise à disposition des données du Bloc 1.

## 2. Position dans le pipeline

Le pipeline complet du Bloc 1 est le suivant :

```text
1. Collecte et extraction multi-sources
2. Analyse qualité des données extraites
3. Nettoyage et normalisation
4. Agrégation finale du dataset IA
5. Modélisation de la base de données
6. Création PostgreSQL
7. Import des données préparées
8. Contrôle qualité en base
9. Mise à disposition via API REST
```

L’API REST intervient donc après l’import et le contrôle qualité de la base PostgreSQL.

## 3. Technologies utilisées

L’API a été développée avec :

```text
FastAPI
Uvicorn
Pydantic
psycopg2-binary
python-dotenv
PostgreSQL
Docker
Swagger / OpenAPI
```

FastAPI a été choisi car il permet :

- de créer rapidement une API REST ;
- de générer automatiquement une documentation Swagger ;
- de valider les réponses avec Pydantic ;
- de gérer facilement les paramètres de requête ;
- d’intégrer une sécurité par clé API ;
- de se connecter à PostgreSQL via Python.

## 4. Structure des fichiers API

La structure mise en place est :

```text
api/
├── __init__.py
├── main.py
├── database.py
├── security.py
├── schemas.py
└── routes/
    ├── __init__.py
    ├── health.py
    ├── lives.py
    ├── sellers.py
    └── analytics.py
```

## 5. Rôle des fichiers

## 5.1. `api/main.py`

Le fichier `main.py` initialise l’application FastAPI.

Il configure :

- le titre de l’API ;
- la description ;
- la version ;
- les tags Swagger ;
- les routes ;
- le middleware CORS ;
- la sécurité des routes protégées.

Il expose aussi une route racine :

```text
GET /
```

Cette route retourne un message simple avec les liens utiles.

## 5.2. `api/database.py`

Le fichier `database.py` centralise la connexion à PostgreSQL.

Il contient les fonctions permettant de :

- charger les variables d’environnement ;
- récupérer la configuration PostgreSQL ;
- ouvrir une connexion ;
- exécuter une requête retournant plusieurs lignes ;
- exécuter une requête retournant une seule ligne ;
- vérifier la disponibilité de la base.

Les requêtes retournent des dictionnaires Python afin d’être facilement converties en JSON par FastAPI.

## 5.3. `api/security.py`

Le fichier `security.py` gère la sécurité de l’API.

La sécurité repose sur une clé API envoyée dans le header HTTP :

```text
X-API-Key
```

Si la clé est absente, l’API retourne :

```text
401 Unauthorized
```

Si la clé est incorrecte, l’API retourne :

```text
403 Forbidden
```

## 5.4. `api/schemas.py`

Le fichier `schemas.py` contient les modèles Pydantic utilisés pour documenter les réponses JSON.

Les principaux modèles sont :

```text
HealthResponse
LiveSalesRow
SellerRow
PlatformSummaryRow
SellerSummaryRow
MessageResponse
```

Ces modèles permettent à Swagger d’afficher clairement la structure des réponses attendues.

## 5.5. `api/routes/health.py`

Ce fichier contient la route de santé :

```text
GET /health
```

Elle vérifie que l’API fonctionne et que la base PostgreSQL est accessible.

## 5.6. `api/routes/lives.py`

Ce fichier contient les routes liées aux lives et au dataset final.

Il permet de consulter les lignes de :

```text
analytics.dataset_final_live_sales
```

## 5.7. `api/routes/sellers.py`

Ce fichier contient les routes liées aux vendeurs.

Il permet de consulter :

- la liste des vendeurs ;
- les lives d’un vendeur ;
- une synthèse de performance par vendeur.

## 5.8. `api/routes/analytics.py`

Ce fichier contient les routes analytiques.

Il permet de consulter :

- les meilleurs lives ;
- les indicateurs par plateforme ;
- les lives avec les meilleurs taux de conversion.

## 6. Configuration de l’environnement

Les paramètres de connexion et la clé API sont définis dans le fichier :

```text
.env
```

Configuration utilisée :

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=paylive_ai_copilot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

API_KEY=paylive-dev-api-key
```

Le fichier `.env.example` documente les mêmes variables :

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=paylive_ai_copilot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

API_KEY=paylive-dev-api-key
```

Le port `5433` correspond au port exposé par Docker pour PostgreSQL.

## 7. Base de données utilisée

L’API se connecte à la base PostgreSQL :

```text
paylive_ai_copilot
```

La base est exécutée dans Docker avec le conteneur :

```text
paylive_postgres
```

Les données exposées proviennent principalement des schémas :

```text
core
analytics
```

## 8. Données exposées

L’API expose principalement le dataset final :

```text
analytics.dataset_final_live_sales
```

Ce dataset contient une ligne par session live.

Il contient des indicateurs comme :

```text
total_comments
purchase_intent_comments
total_carts
paid_carts
total_orders
total_revenue
payment_success_rate
conversion_rate
revenue_per_viewer
top_product_category
api_error_events
```

L’API expose également certaines données du schéma `core`, notamment :

```text
core.sellers
```

## 9. Sécurité par clé API

Les routes principales sont protégées par clé API.

Le client doit envoyer le header :

```text
X-API-Key: paylive-dev-api-key
```

Exemple :

```bash
curl -H "X-API-Key: paylive-dev-api-key" http://127.0.0.1:8000/api/v1/sellers
```

La route `/health` reste publique afin de pouvoir vérifier l’état de l’API sans authentification.

## 10. Routes publiques

## 10.1. Route racine

```text
GET /
```

Cette route retourne les informations générales de l’API :

```json
{
  "application": "PayLive AI Copilot API",
  "version": "1.0.0",
  "documentation_url": "/docs",
  "health_url": "/health"
}
```

## 10.2. Health check

```text
GET /health
```

Cette route vérifie :

- que l’API est disponible ;
- que PostgreSQL est accessible.

Réponse attendue :

```json
{
  "status": "ok",
  "application": "PayLive AI Copilot API",
  "database_available": true,
  "database_name": "paylive_ai_copilot"
}
```

## 11. Routes protégées

Toutes les routes suivantes nécessitent le header :

```text
X-API-Key
```

## 11.1. Liste des lives

```text
GET /api/v1/lives
```

Cette route retourne les lignes du dataset final agrégé.

Paramètres disponibles :

```text
platform
seller_id
min_revenue
limit
offset
```

Exemple :

```text
GET /api/v1/lives?limit=5&offset=0
```

Exemple avec filtre :

```text
GET /api/v1/lives?platform=instagram&limit=5&offset=0
```

Cette route lit la table :

```text
analytics.dataset_final_live_sales
```

## 11.2. Détail d’un live

```text
GET /api/v1/lives/{live_id}
```

Cette route retourne une ligne du dataset final à partir de son identifiant `live_id`.

Exemple :

```text
GET /api/v1/lives/LIVE0001
```

Si le live n’existe pas, l’API retourne :

```text
404 Not Found
```

## 11.3. Liste des vendeurs

```text
GET /api/v1/sellers
```

Cette route retourne les vendeurs présents dans la table :

```text
core.sellers
```

Paramètres disponibles :

```text
limit
offset
```

Exemple :

```text
GET /api/v1/sellers?limit=5&offset=0
```

## 11.4. Lives d’un vendeur

```text
GET /api/v1/sellers/{seller_id}/lives
```

Cette route retourne les lives associés à un vendeur.

Exemple :

```text
GET /api/v1/sellers/SEL0001/lives
```

Si le vendeur n’existe pas, l’API retourne :

```text
404 Not Found
```

## 11.5. Synthèse de performance par vendeur

```text
GET /api/v1/sellers/summary/performance
```

Cette route retourne une synthèse de performance par vendeur.

Indicateurs retournés :

```text
seller_id
shop_name
live_count
total_revenue
average_revenue
average_conversion_rate
```

## 11.6. Top lives

```text
GET /api/v1/analytics/top-lives
```

Cette route retourne les lives les plus performants selon une métrique.

Paramètres disponibles :

```text
metric
platform
limit
```

Métriques acceptées :

```text
total_revenue
conversion_rate
total_comments
paid_carts
```

Exemple :

```text
GET /api/v1/analytics/top-lives?metric=total_revenue&limit=5
```

## 11.7. Synthèse par plateforme

```text
GET /api/v1/analytics/platform-summary
```

Cette route retourne une agrégation par plateforme.

Indicateurs retournés :

```text
platform
live_count
total_revenue
average_revenue
average_conversion_rate
total_comments
total_carts
total_orders
```

## 11.8. Insights conversion

```text
GET /api/v1/analytics/conversion-insights
```

Cette route retourne les lives avec les meilleurs taux de conversion.

Paramètres disponibles :

```text
min_peak_viewers
limit
```

Exemple :

```text
GET /api/v1/analytics/conversion-insights?min_peak_viewers=1&limit=10
```

## 12. Documentation Swagger

FastAPI génère automatiquement la documentation Swagger.

Elle est accessible à l’adresse :

```text
http://127.0.0.1:8000/docs
```

Swagger permet de :

- visualiser toutes les routes ;
- voir les paramètres attendus ;
- consulter les modèles de réponse ;
- tester les routes directement ;
- envoyer la clé API via le bouton `Authorize`.

## 13. Documentation OpenAPI

Le schéma OpenAPI est disponible à l’adresse :

```text
http://127.0.0.1:8000/openapi.json
```

Ce fichier décrit toute l’API au format JSON.

Il peut être utilisé pour :

- générer une documentation externe ;
- tester l’API ;
- intégrer l’API à un autre outil ;
- prouver que l’API est documentée automatiquement.

## 14. Lancement de l’API

Avant de lancer l’API, il faut vérifier que PostgreSQL est actif :

```bash
docker ps
```

Les conteneurs attendus sont :

```text
paylive_postgres
paylive_pgadmin
```

Ensuite, lancer FastAPI avec Uvicorn :

```bash
python -m uvicorn api.main:app --reload
```

L’API est disponible sur :

```text
http://127.0.0.1:8000
```

## 15. Tests réalisés avec Swagger

Les routes ont été testées depuis Swagger.

Pour les routes protégées, il faut cliquer sur :

```text
Authorize
```

Puis renseigner :

```text
paylive-dev-api-key
```

Swagger ajoute alors automatiquement le header :

```text
X-API-Key: paylive-dev-api-key
```

Exemple de test validé :

```text
GET /api/v1/sellers
```

Résultat obtenu :

```json
[
  {
    "seller_id": "SEL0001",
    "shop_name": "LiveShop_1",
    "country": "Maroc",
    "main_platform": "instagram",
    "seller_status": "inactive",
    "created_at": "2025-01-29T04:47:06"
  }
]
```

Le code HTTP obtenu est :

```text
200
```

Cela confirme que :

- Swagger envoie bien la clé API ;
- FastAPI valide la clé ;
- l’API interroge PostgreSQL ;
- la réponse JSON est correctement retournée.

## 16. Tests réalisés avec PowerShell

Exemple de test PowerShell :

```powershell
$headers = @{ "X-API-Key" = "paylive-dev-api-key" }

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/sellers?limit=5&offset=0" `
  -Headers $headers
```

Exemple pour les lives :

```powershell
$headers = @{ "X-API-Key" = "paylive-dev-api-key" }

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/lives?limit=5&offset=0" `
  -Headers $headers
```

## 17. Gestion des erreurs

L’API gère plusieurs erreurs.

## 17.1. Clé API manquante

Si le header `X-API-Key` est absent :

```json
{
  "detail": "Missing API key. Please provide the X-API-Key header."
}
```

Code HTTP :

```text
401 Unauthorized
```

## 17.2. Clé API invalide

Si la clé API est incorrecte :

```json
{
  "detail": "Invalid API key."
}
```

Code HTTP :

```text
403 Forbidden
```

## 17.3. Ressource inexistante

Si un live ou un vendeur demandé n’existe pas :

```json
{
  "detail": "Live not found: LIVE0001"
}
```

ou :

```json
{
  "detail": "Seller not found: SEL0001"
}
```

Code HTTP :

```text
404 Not Found
```

## 18. Point important sur le navigateur

Lorsqu’une route protégée est ouverte directement dans la barre d’adresse du navigateur, le header `X-API-Key` n’est pas envoyé.

Exemple :

```text
http://127.0.0.1:8000/api/v1/sellers
```

Dans ce cas, l’API retourne :

```json
{
  "detail": "Missing API key. Please provide the X-API-Key header."
}
```

Ce comportement est normal.

Pour tester les routes protégées, il faut utiliser :

```text
Swagger
PowerShell
curl
Postman
```

## 19. Problème rencontré pendant les tests

Pendant les premiers tests, la route suivante retournait une liste vide :

```text
GET /api/v1/lives
```

La cause n’était pas l’API, mais l’import du dataset final dans PostgreSQL.

Le rapport d’import indiquait l’erreur suivante :

```text
invalid input syntax for type integer: "3.0"
CONTEXT: COPY dataset_final_live_sales, line 2, column total_orders: "3.0"
```

Le fichier CSV final contenait bien des lignes, mais certaines colonnes attendues comme entiers contenaient des valeurs au format décimal, par exemple :

```text
3.0
```

PostgreSQL attendait une valeur entière :

```text
3
```

La correction a été faite dans le script :

```text
src/data_processing/build_final_ai_dataset.py
```

Les colonnes de comptage du dataset final ont été explicitement converties en entiers avant l’export CSV.

Après correction :

- le dataset final a été régénéré ;
- les données ont été réimportées ;
- le contrôle qualité base a été relancé ;
- la route `/api/v1/lives` a fonctionné correctement.

## 20. Contrôles réalisés avant validation de l’API

Avant validation de l’API, les éléments suivants ont été vérifiés :

```text
PostgreSQL actif dans Docker
base paylive_ai_copilot disponible
données importées dans core
dataset final importé dans analytics
contrôle qualité base exécuté
clé API définie dans .env
Swagger accessible
routes protégées testées avec X-API-Key
réponses JSON retournées
```

## 21. Exemples de réponses

## 21.1. Réponse vendeur

```json
{
  "seller_id": "SEL0001",
  "shop_name": "LiveShop_1",
  "country": "Maroc",
  "main_platform": "instagram",
  "seller_status": "inactive",
  "created_at": "2025-01-29T04:47:06"
}
```

## 21.2. Réponse analytique plateforme

```json
{
  "platform": "instagram",
  "live_count": 10,
  "total_revenue": 1250.50,
  "average_revenue": 125.05,
  "average_conversion_rate": 0.0321,
  "total_comments": 450,
  "total_carts": 80,
  "total_orders": 35
}
```

## 21.3. Réponse live

```json
{
  "live_id": "LIVE0001",
  "seller_id": "SEL0001",
  "platform": "instagram",
  "live_date": "2025-01-29",
  "peak_viewers": 500,
  "total_comments": 120,
  "total_carts": 20,
  "total_orders": 8,
  "total_revenue": 320.50,
  "payment_success_rate": 0.8,
  "conversion_rate": 0.04,
  "final_dataset_status": "ready_for_ai"
}
```

## 22. Intérêt pour le projet

Cette API permet de mettre à disposition les données préparées du projet.

Elle permet à un client externe, un tableau de bord ou une application web de récupérer les données sans accéder directement aux fichiers CSV ou à la base PostgreSQL.

Elle apporte :

```text
mise à disposition des données
accès structuré aux indicateurs
sécurité par clé API
documentation automatique
réponses JSON
connexion à PostgreSQL
séparation claire entre base et consommateurs de données
```

## 23. Lien avec le Bloc 2

Le dataset final exposé par l’API pourra être réutilisé pour la suite IA.

Exemples :

```text
récupérer les lives les plus performants
analyser les taux de conversion
alimenter un modèle de prédiction
fournir des indicateurs à un tableau de bord
exposer les résultats d’un futur modèle IA
```

L’API pourra évoluer pour exposer plus tard :

```text
des prédictions IA
des scores d’intention d’achat
des recommandations produit
des alertes commerciales
```

## 24. Limites

L’API actuelle est une version projet.

Certaines limites sont assumées :

- authentification simple par clé API ;
- pas de gestion d’utilisateurs avancée ;
- pas encore de pagination complète avec métadonnées ;
- pas encore de tests automatisés complets ;
- pas encore de déploiement cloud ;
- données simulées uniquement.

Ces limites pourront être améliorées dans les étapes suivantes.

## 25. Prochaine étape

Après la documentation de l’API, les prochaines étapes prévues sont :

```text
1. Tests automatisés de l’API
2. Registre RGPD
3. Mise à jour du README global
4. Vérification finale du Bloc 1
```

## 26. Conclusion

L’API REST FastAPI permet de mettre à disposition les données nettoyées, agrégées et stockées dans PostgreSQL.

Elle expose des endpoints documentés, sécurisés par clé API et testables via Swagger.

Cette étape finalise la mise à disposition des données du Bloc 1 et prépare les futures fonctionnalités IA du projet PayLive AI Copilot.