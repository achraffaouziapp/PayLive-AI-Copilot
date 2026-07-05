# Architecture application — Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document décrit l’architecture technique de l’application web développée dans le cadre du Bloc 3 du projet **PayLive AI Copilot**.

L’objectif du Bloc 3 est d’intégrer le service IA réalisé dans le Bloc 2 dans une application utilisable par un vendeur en live shopping.

L’application permet à un utilisateur de :

```text
saisir un commentaire de live ;
envoyer ce commentaire au service IA ;
obtenir l’intention prédite ;
consulter le score de confiance ;
visualiser les informations du modèle ;
visualiser les métriques du modèle ;
ouvrir le dashboard de monitoring IA ;
télécharger les alertes de monitoring.
```

L’application est développée en **HTML, CSS et JavaScript natif**.  
Elle est servie par **Nginx** dans un conteneur Docker et communique avec l’API FastAPI existante.

## 2. Synthèse de l’architecture retenue

L’architecture retenue est une architecture web légère en plusieurs couches.

```text
Utilisateur navigateur
        ↓
Frontend HTML / CSS / JavaScript
        ↓ HTTP via proxy Nginx
API FastAPI
        ↓
Service IA
        ↓
Modèle local TF-IDF + Logistic Regression
        ↓
Logs, métriques, dashboard et alertes
```

Cette architecture est cohérente avec les Blocs 1 et 2 :

```text
Bloc 1 : données, PostgreSQL, API REST
Bloc 2 : service IA, modèle, monitoring, dashboard, CI MLOps
Bloc 3 : application web intégrant le service IA
```

## 3. Architecture n-tiers

L’application suit une architecture **n-tiers légère**.

| Couche | Composant | Rôle |
|---|---|---|
| Présentation | Frontend HTML/CSS/JS | Interface utilisateur |
| Serveur statique | Nginx | Sert les fichiers du frontend et proxifie les appels API |
| Application backend | FastAPI | Expose les routes REST données et IA |
| Service IA | Modules Python `src/ai/` | Charge le modèle, prédit l’intention, journalise les prédictions |
| Données | PostgreSQL + fichiers CSV | Stocke les données métier et les rapports |
| Monitoring | CSV + dashboard HTML | Suit les prédictions, les alertes et les métriques |

Cette approche permet de séparer clairement :

```text
l’interface utilisateur ;
la logique API ;
le modèle IA ;
les données ;
le monitoring.
```

## 4. Architecture Docker

L’application est exécutée avec Docker Compose.

```text
Docker Compose
├── postgres
│   └── base PostgreSQL paylive_ai_copilot
├── pgadmin
│   └── interface d’administration PostgreSQL
├── api
│   └── FastAPI + routes données + routes IA + monitoring
└── frontend
    └── Nginx + fichiers HTML/CSS/JS
```

Ports utilisés :

| Service | Port hôte | Port conteneur | Usage |
|---|---:|---:|---|
| PostgreSQL | 5433 | 5432 | Base de données |
| pgAdmin | 5050 | 80 | Administration PostgreSQL |
| API FastAPI | 8000 | 8000 | Backend et service IA |
| Frontend | 8080 | 80 | Application web |

Commandes principales :

```bash
docker compose up -d --build
docker compose ps
docker logs --tail 80 paylive_frontend
docker logs --tail 80 paylive_api
```

## 5. Structure réelle du frontend

La structure retenue dans le projet est la suivante :

```text
frontend/
├── Dockerfile
├── nginx.conf
├── index.html
├── css/
│   └── styles.css
└── js/
    └── app.js
```

Rôle des fichiers :

| Fichier | Rôle |
|---|---|
| `frontend/index.html` | Structure de l’interface utilisateur |
| `frontend/css/styles.css` | Mise en forme, responsive design et lisibilité |
| `frontend/js/app.js` | Appels API, gestion des événements et affichage dynamique |
| `frontend/Dockerfile` | Construction de l’image Docker du frontend |
| `frontend/nginx.conf` | Configuration Nginx et proxy vers l’API |
| `docker-compose.yml` | Orchestration des conteneurs frontend, API, PostgreSQL et pgAdmin |

## 6. Choix techniques

| Sujet | Choix | Justification |
|---|---|---|
| Langage interface | HTML, CSS, JavaScript natif | Simple, léger, rapide à développer et démontrable |
| Framework front | Aucun framework | Évite une complexité inutile pour une preuve de concept |
| Serveur frontend | Nginx | Léger, stable, adapté au service de fichiers statiques |
| Backend | FastAPI | Déjà utilisé dans les Blocs 1 et 2 |
| Modèle IA | TF-IDF + Logistic Regression | Modèle local, explicable et intégré dans l’API |
| Authentification | `X-API-Key` | Cohérent avec la sécurité API existante |
| Conteneurisation | Docker Compose | Lancement homogène des services |
| CI/CD | GitHub Actions | Automatisation des tests et validation du build Docker |
| Monitoring | Dashboard HTML + alertes CSV | Solution légère et adaptée au projet |

## 7. Routes API exploitées par l’application

L’application frontend consomme les routes suivantes :

| Fonction | Méthode | Route |
|---|---|---|
| Santé API | GET | `/health` |
| Prédiction simple | POST | `/api/v1/ai/predict-intent` |
| Informations modèle | GET | `/api/v1/ai/model-info` |
| Métriques modèle | GET | `/api/v1/ai/model-metrics` |
| Dashboard monitoring | GET | `/api/v1/ai/monitoring/dashboard` |
| Alertes monitoring | GET | `/api/v1/ai/monitoring/alerts` |

Les routes IA sont protégées par le header :

```text
X-API-Key: paylive-dev-api-key
```

Le test de connexion de l’interface utilise une route protégée afin de vérifier que la clé API est valide.

## 8. Flux de données principaux

### 8.1. Flux de prédiction simple

```text
Utilisateur
  ↓ saisit un commentaire
Frontend JavaScript
  ↓ POST /api/v1/ai/predict-intent avec X-API-Key
API FastAPI
  ↓ appelle api.ai_service
Module IA
  ↓ charge le modèle via intent_predictor.py
Modèle IA
  ↓ prédit l’intention et le score de confiance
API FastAPI
  ↓ retourne une réponse JSON
Frontend JavaScript
  ↓ affiche l’intention, la confiance, le temps de réponse et la version du modèle
```

### 8.2. Flux de consultation des informations modèle

```text
Utilisateur
  ↓ clique sur “Charger les informations”
Frontend JavaScript
  ↓ GET /api/v1/ai/model-info
API FastAPI
  ↓ lit les métadonnées du modèle
Frontend JavaScript
  ↓ affiche le JSON dans l’interface
```

### 8.3. Flux de consultation des métriques modèle

```text
Utilisateur
  ↓ clique sur “Charger les métriques”
Frontend JavaScript
  ↓ GET /api/v1/ai/model-metrics
API FastAPI
  ↓ lit les rapports d’évaluation et de benchmark
Frontend JavaScript
  ↓ affiche les métriques dans l’interface
```

### 8.4. Flux de monitoring

```text
Utilisateur
  ↓ clique sur “Ouvrir le dashboard”
Frontend JavaScript
  ↓ GET /api/v1/ai/monitoring/dashboard
API FastAPI
  ↓ régénère le dashboard et les alertes
Fichiers de monitoring
  ↓ HTML ou CSV
Frontend JavaScript
  ↓ ouvre le dashboard ou télécharge les alertes
```

## 9. Zones de stockage

| Élément | Zone de stockage |
|---|---|
| Données brutes | `data/raw/` |
| Données intermédiaires | `data/interim/` |
| Données nettoyées | `data/processed/` |
| Dataset NLP IA | `data/ai/datasets/` |
| Artefacts modèle IA | `models/intent_classifier/` |
| Logs de prédictions IA | `data/ai/predictions/ai_predictions_log.csv` |
| Rapports IA | `data/ai/reports/` |
| Dashboard monitoring | `data/ai/reports/model_monitoring_dashboard.html` |
| Alertes monitoring | `data/ai/reports/model_monitoring_alerts.csv` |
| Frontend | `frontend/` |
| Documentation Bloc 3 | `docs/08_application/` |
| Workflow CI/CD | `.github/workflows/ai_mlops_ci.yml` |

## 10. Modélisation des objets manipulés par l’application

L’application frontend ne stocke pas les données en base.  
Elle manipule des objets JSON échangés avec l’API.

### 10.1. Objet `PredictionRequest`

```json
{
  "comment_text": "je prends la robe noire en M"
}
```

| Champ | Type | Description |
|---|---|---|
| `comment_text` | string | Commentaire saisi par l’utilisateur |

### 10.2. Objet `PredictionResponse`

```json
{
  "comment_text": "je prends la robe noire en M",
  "predicted_intent": "purchase_intent",
  "confidence_score": 0.25,
  "is_low_confidence": true,
  "low_confidence_threshold": 0.6,
  "response_time_ms": 45.12,
  "model_version": "intent_classifier_v1"
}
```

| Champ | Type | Description |
|---|---|---|
| `comment_text` | string | Texte analysé |
| `predicted_intent` | string | Intention prédite par le modèle |
| `confidence_score` | number | Score de confiance |
| `is_low_confidence` | boolean | Indique si la prédiction est incertaine |
| `low_confidence_threshold` | number | Seuil utilisé pour l’alerte |
| `response_time_ms` | number | Temps de réponse du service IA |
| `model_version` | string | Version du modèle utilisé |

### 10.3. Objet `ModelInfo`

```json
{
  "model_name": "intent_classifier",
  "model_type": "TF-IDF + Logistic Regression",
  "model_version": "intent_classifier_v1",
  "classes": [
    "purchase_intent",
    "product_question",
    "payment_question",
    "shipping_question",
    "other",
    "unknown"
  ]
}
```

### 10.4. Objet `MonitoringAlert`

```json
{
  "timestamp": "2026-07-05T10:00:00",
  "comment_text": "je prends la robe noire en M",
  "predicted_intent": "purchase_intent",
  "confidence_score": 0.42,
  "alert_type": "LOW_CONFIDENCE",
  "alert_message": "Score de confiance inférieur au seuil"
}
```

## 11. Parcours utilisateur fonctionnel

### 11.1. Parcours nominal

```text
1. L’utilisateur ouvre http://127.0.0.1:8080.
2. Il vérifie l’URL API et la clé API.
3. Il clique sur “Tester la connexion”.
4. L’application confirme que l’API IA est disponible et que la clé API est valide.
5. Il saisit un commentaire de live.
6. Il clique sur “Analyser le commentaire”.
7. L’application affiche l’intention prédite.
8. L’application affiche le score de confiance.
9. Si le score est faible, une alerte textuelle est affichée.
```

### 11.2. Parcours d’erreur avec clé API invalide

```text
1. L’utilisateur saisit une clé API incorrecte.
2. Il clique sur “Tester la connexion”.
3. L’application appelle une route protégée.
4. L’API retourne une erreur 403.
5. L’interface affiche “Clé API invalide”.
```

### 11.3. Parcours monitoring

```text
1. L’utilisateur clique sur “Ouvrir le dashboard”.
2. L’API régénère le dashboard de monitoring.
3. Le dashboard HTML est ouvert dans un nouvel onglet.
4. L’utilisateur peut aussi télécharger les alertes au format CSV.
```

## 12. Wireframe textuel de l’interface

```text
┌───────────────────────────────────────────────────────────────┐
│ PayLive AI Copilot                         Bloc 3 Application │
├───────────────────────────────────────────────────────────────┤
│ Configuration API                                             │
│ [URL API] [Clé API] [Enregistrer] [Tester la connexion]       │
├───────────────────────────────────────────────────────────────┤
│ Prédiction d’intention                                        │
│ [Zone commentaire]                                            │
│ [Analyser le commentaire] [Réinitialiser]                     │
│                                                               │
│ Résultat IA                                                   │
│ Intention | Confiance | Temps réponse | Version modèle        │
├───────────────────────────────────────────────────────────────┤
│ Informations modèle                                           │
│ [Charger les informations]                                    │
│ [JSON affiché]                                                │
├───────────────────────────────────────────────────────────────┤
│ Métriques modèle                                              │
│ [Charger les métriques]                                       │
│ [JSON affiché]                                                │
├───────────────────────────────────────────────────────────────┤
│ Monitoring IA                                                 │
│ [Ouvrir le dashboard] [Télécharger les alertes CSV]           │
└───────────────────────────────────────────────────────────────┘
```

## 13. Gestion des erreurs

| Erreur | Cause probable | Comportement attendu |
|---|---|---|
| 401 | clé API absente | afficher un message indiquant que la clé API est absente |
| 403 | clé API invalide | afficher “Clé API invalide” |
| 422 | commentaire vide ou payload invalide | afficher un message de validation |
| 500 | erreur serveur | afficher une erreur serveur lisible |
| Network error | API arrêtée, frontend mal configuré ou proxy indisponible | afficher “API inaccessible” |

Une correction importante a été apportée : le bouton “Tester la connexion” ne teste plus uniquement `/health`, car cette route est publique.  
Il teste maintenant une route protégée afin de valider réellement la clé API.

## 14. Sécurité et bonnes pratiques OWASP

Mesures appliquées :

| Risque | Mesure |
|---|---|
| Accès non autorisé aux routes IA | Header `X-API-Key` obligatoire |
| Mauvaise clé API | Retour 403 côté API et message explicite côté interface |
| Données sensibles | Données simulées uniquement |
| Exposition excessive | Réponses limitées aux informations nécessaires |
| Entrées invalides | Validation côté interface et côté API |
| Dépendance externe IA | Aucune donnée envoyée à un fournisseur IA externe |
| Mauvaise configuration réseau | Proxy Nginx vers l’API Docker |
| Traçabilité insuffisante | Logs Docker, logs de prédictions, dashboard et alertes |

Limites de la preuve de concept :

```text
pas de gestion multi-utilisateur ;
pas de rôles avancés ;
pas de JWT ;
clé API préremplie pour faciliter la démonstration locale.
```

Évolution possible :

```text
remplacer X-API-Key par JWT ou OAuth2 dans une version production.
```

## 15. Accessibilité technique

L’application intègre des objectifs d’accessibilité dès la conception.

Mesures prévues ou appliquées :

- déclaration `lang="fr"` ;
- utilisation d’une balise `<main>` ;
- champs associés à des `<label>` ;
- boutons HTML natifs ;
- messages dynamiques avec `aria-live` ;
- textes d’erreur explicites ;
- mise en page responsive ;
- sections séparées pour améliorer la lisibilité ;
- contraste suffisant entre texte et arrière-plan ;
- navigation possible au clavier.

Les tests manuels d’accessibilité vérifient notamment :

```text
navigation au clavier ;
lisibilité des messages ;
présence des labels ;
comportement responsive ;
visibilité du focus ;
compréhension des alertes.
```

## 16. Configuration Nginx

Le frontend est servi par Nginx.

La configuration permet :

```text
de servir index.html ;
de servir les fichiers CSS et JS ;
de proxifier /health vers l’API ;
de proxifier /api/ vers l’API.
```

Exemple de configuration :

```nginx
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /health {
        proxy_pass http://api:8000/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://api:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Grâce au proxy, le frontend peut utiliser des URLs relatives comme :

```text
/api/v1/ai
/health
```

## 17. Configuration Docker du frontend

### 17.1. Dockerfile

```dockerfile
FROM nginx:1.27-alpine

COPY index.html /usr/share/nginx/html/index.html
COPY css /usr/share/nginx/html/css
COPY js /usr/share/nginx/html/js
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

### 17.2. Service Docker Compose

```yaml
frontend:
  build:
    context: ./frontend
  container_name: paylive_frontend
  restart: unless-stopped
  ports:
    - "8080:80"
  depends_on:
    - api
```

## 18. Tests et intégration continue

Des tests frontend statiques sont ajoutés dans :

```text
tests/test_frontend_static.py
```

Ils vérifient notamment :

```text
présence des fichiers frontend ;
présence des sections principales ;
présence des routes API utilisées ;
présence du header X-API-Key ;
validation de la clé API sur une route protégée ;
règles CSS responsive ;
configuration Nginx ;
Dockerfile frontend.
```

La chaîne GitHub Actions exécute les tests et valide le build Docker frontend :

```text
.github/workflows/ai_mlops_ci.yml
```

Étapes concernées :

```text
pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py tests/test_frontend_static.py -v
docker compose build frontend
```

## 19. Preuve de concept réalisée

La preuve de concept est opérationnelle.

Elle démontre :

```text
l’ouverture de l’application sur http://127.0.0.1:8080 ;
la connexion au backend FastAPI ;
la validation de la clé API ;
l’appel au modèle IA ;
l’affichage de la prédiction ;
l’affichage du score de confiance ;
l’accès aux informations modèle ;
l’accès aux métriques modèle ;
l’ouverture du dashboard monitoring ;
le téléchargement des alertes CSV ;
le fonctionnement dans Docker ;
la validation par GitHub Actions.
```

## 20. Critères de validation technique

| Critère | Commande ou preuve | Statut attendu |
|---|---|---|
| Frontend lancé | `docker compose up -d --build` | OK |
| Conteneur frontend actif | `docker compose ps` | OK |
| Application visible | `http://127.0.0.1:8080` | OK |
| API accessible | `http://127.0.0.1:8000/health` | OK |
| Appel IA fonctionnel | prédiction depuis l’interface | OK |
| Clé API invalide gérée | test avec mauvaise clé | OK |
| Dashboard accessible | bouton dashboard | OK |
| Alertes accessibles | téléchargement CSV | OK |
| Tests frontend | `pytest tests/test_frontend_static.py -v` | OK |
| CI verte | GitHub Actions | OK |

## 21. Limites et évolutions

Limites de la version actuelle :

```text
interface volontairement simple ;
pas de framework front avancé ;
pas de gestion multi-utilisateur ;
pas de rôles ou groupes ;
pas de stockage applicatif côté frontend ;
pas de déploiement cloud ;
clé API de démonstration préremplie.
```

Évolutions possibles :

```text
ajouter une authentification JWT ;
ajouter des rôles vendeur, admin et analyste ;
ajouter une vraie page historique ;
ajouter un tableau de bord commercial ;
ajouter des tests end-to-end avec Playwright ;
ajouter un déploiement de préproduction ;
ajouter une supervision applicative plus avancée.
```

## 22. Conclusion

L’architecture du Bloc 3 permet de démontrer l’intégration concrète du service IA dans une application web.

Le choix d’un frontend HTML/CSS/JavaScript natif servi par Nginx est adapté au contexte du projet :

```text
solution légère ;
facile à conteneuriser ;
facile à expliquer ;
compatible avec Docker Compose ;
connectée à l’API IA existante ;
testable automatiquement ;
intégrée à la CI GitHub Actions.
```

L’application constitue une preuve de concept fonctionnelle, accessible localement et cohérente avec les réalisations des Blocs 1 et 2.
