# Architecture application — Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document décrit l’architecture technique de l’application web du Bloc 3.

L’application sera développée en **HTML + CSS + JavaScript natif** et servie dans un conteneur Docker via **Nginx**.

Elle consommera l’API FastAPI déjà développée dans les Blocs 1 et 2.

## 2. Vue d’ensemble

```text
Utilisateur navigateur
        ↓
Frontend HTML/CSS/JS
        ↓ HTTP + X-API-Key
API FastAPI
        ↓
Service IA
        ↓
Modèle local TF-IDF + Logistic Regression
        ↓
Logs, rapports, dashboard et alertes
```

## 3. Architecture Docker cible

```text
Docker Compose
├── postgres
│   └── base PostgreSQL paylive_ai_copilot
├── pgadmin
│   └── interface d’administration PostgreSQL
├── api
│   └── FastAPI + routes données + routes IA
└── frontend
    └── Nginx + fichiers HTML/CSS/JS
```

Ports prévus :

| Service | Port hôte | Port conteneur | Usage |
|---|---:|---:|---|
| PostgreSQL | 5433 | 5432 | Base de données |
| pgAdmin | 5050 | 80 | Administration DB |
| API FastAPI | 8000 | 8000 | Backend et service IA |
| Frontend | 8080 | 80 | Application web |

## 4. Architecture applicative

L’application front est une application statique.

Elle contient :

```text
frontend/
├── Dockerfile
├── nginx.conf
└── public/
    ├── index.html
    └── assets/
        ├── css/
        │   └── styles.css
        └── js/
            ├── config.js
            └── app.js
```

Rôle des fichiers :

| Fichier | Rôle |
|---|---|
| `index.html` | Structure de l’interface utilisateur |
| `styles.css` | Mise en forme, responsive et lisibilité |
| `config.js` | URL de l’API, routes et constantes |
| `app.js` | Appels API, gestion des événements et affichage |
| `Dockerfile` | Construction de l’image frontend |
| `nginx.conf` | Configuration du serveur statique |

## 5. Flux de données

### 5.1. Prédiction simple

```text
Utilisateur
  ↓ saisit un commentaire
Frontend JS
  ↓ POST /api/v1/ai/predict-intent
API FastAPI
  ↓ appelle intent_predictor.py
Modèle IA
  ↓ retourne intention + confiance
API FastAPI
  ↓ JSON
Frontend JS
  ↓ affiche le résultat
```

### 5.2. Prédiction batch

```text
Utilisateur
  ↓ saisit plusieurs commentaires
Frontend JS
  ↓ POST /api/v1/ai/batch-predict-intents
API FastAPI
  ↓ exécute predict_batch
Modèle IA
  ↓ retourne plusieurs prédictions
Frontend JS
  ↓ affiche un tableau de résultats
```

### 5.3. Monitoring

```text
Frontend JS
  ↓ GET /api/v1/ai/monitoring/dashboard
API FastAPI
  ↓ régénère dashboard + alertes
Fichiers de monitoring
  ↓ HTML ou CSV
Frontend JS
  ↓ affiche ou télécharge la preuve
```

## 6. Routes API exploitées

| Fonction | Méthode | Route |
|---|---|---|
| Santé API | GET | `/health` |
| Prédiction simple | POST | `/api/v1/ai/predict-intent` |
| Prédiction batch | POST | `/api/v1/ai/batch-predict-intents` |
| Informations modèle | GET | `/api/v1/ai/model-info` |
| Métriques modèle | GET | `/api/v1/ai/model-metrics` |
| Dashboard monitoring | GET | `/api/v1/ai/monitoring/dashboard` |
| Alertes monitoring | GET | `/api/v1/ai/monitoring/alerts` |

Toutes les routes IA protégées utilisent :

```text
X-API-Key: paylive-dev-api-key
```

## 7. Gestion CORS

Comme l’application front est servie depuis :

```text
http://localhost:8080
```

et l’API depuis :

```text
http://localhost:8000
```

il faut autoriser les appels cross-origin dans FastAPI.

Configuration recommandée dans `api/main.py` :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Cette configuration est adaptée à la preuve de concept locale.

En production, les origines devront être limitées au domaine réel de l’application.

## 8. Configuration Docker du frontend

### 8.1. Dockerfile prévu

```dockerfile
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY public /usr/share/nginx/html

EXPOSE 80
```

### 8.2. Configuration Nginx prévue

```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 8.3. Ajout dans `docker-compose.yml`

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

## 9. Choix techniques

| Sujet | Choix | Justification |
|---|---|---|
| Langage interface | HTML, CSS, JavaScript | Simple, léger, démontrable |
| Framework front | Aucun | Évite une complexité inutile |
| Serveur statique | Nginx | Léger et adapté à Docker |
| Backend | FastAPI | Déjà utilisé dans les Blocs 1 et 2 |
| Authentification | `X-API-Key` | Cohérent avec l’API existante |
| Conteneurisation | Docker Compose | Démarrage homogène des services |
| Monitoring | Dashboard HTML + alertes CSV | Déjà disponible depuis le Bloc 2 |

## 10. Zones de stockage

| Élément | Zone de stockage |
|---|---|
| Données nettoyées | `data/processed/` |
| Dataset IA | `data/ai/datasets/` |
| Artefacts modèle | `models/intent_classifier/` |
| Logs de prédiction | `data/ai/predictions/` |
| Rapports IA | `data/ai/reports/` |
| Frontend | `frontend/public/` |
| Documentation | `docs/08_application/` |

## 11. Gestion des erreurs

L’application doit gérer :

| Erreur | Cause probable | Comportement attendu |
|---|---|---|
| 401 | clé API absente | afficher “clé API manquante” |
| 403 | clé API invalide | afficher “clé API invalide” |
| 422 | payload invalide | afficher “données envoyées invalides” |
| 500 | erreur serveur | afficher “erreur serveur” |
| Network error | API arrêtée ou CORS | afficher “API inaccessible” |

## 12. Sécurité

Mesures prévues :

- API protégée par `X-API-Key` ;
- clé API non versionnée dans les fichiers sensibles ;
- aucune donnée réelle ;
- commentaires de démonstration fictifs ;
- messages d’erreur contrôlés ;
- pas de stockage permanent des commentaires côté navigateur ;
- pas de communication avec un fournisseur IA externe.

## 13. Accessibilité technique

L’architecture front devra faciliter :

- l’utilisation au clavier ;
- la lecture par lecteurs d’écran ;
- la présence de labels sur les champs ;
- la mise en évidence du focus ;
- des messages d’erreur visibles ;
- l’usage de `aria-live` pour les résultats dynamiques ;
- une structure HTML sémantique.

## 14. Critères de validation technique

| Critère | Commande ou preuve |
|---|---|
| Frontend lancé | `docker compose up -d frontend` |
| Application visible | `http://localhost:8080` |
| API accessible | `http://localhost:8000/health` |
| Appel IA fonctionnel | Prédiction affichée dans l’interface |
| Dashboard accessible | Bouton dashboard fonctionnel |
| Alertes accessibles | Téléchargement ou affichage CSV |
| Logs Docker OK | `docker logs paylive_frontend` et `docker logs paylive_api` |

## 15. Conclusion

L’architecture retenue est adaptée au Bloc 3 car elle permet de réaliser une application simple, démontrable et intégrée au service IA existant.

Elle respecte les contraintes du projet :

- solution locale ;
- conteneurisation Docker ;
- intégration API IA ;
- interface accessible ;
- faible complexité ;
- cohérence avec les Blocs 1 et 2.
