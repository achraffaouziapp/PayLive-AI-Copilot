# Développement de l’interface — Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document décrit le développement de l’interface web du Bloc 3 du projet **PayLive AI Copilot**.

L’objectif est de construire une application simple en **HTML, CSS et JavaScript**, conteneurisée avec **Docker** et servie par **Nginx**, capable de consommer l’API IA développée dans le Bloc 2.

L’application permet à un vendeur ou à un démonstrateur de :

```text
saisir un commentaire de live shopping ;
appeler le service IA de prédiction d’intention ;
afficher l’intention prédite ;
afficher le score de confiance ;
afficher une alerte si la prédiction est incertaine ;
consulter les informations du modèle ;
consulter les métriques du modèle ;
ouvrir le dashboard de monitoring IA ;
télécharger les alertes de monitoring.
```

Cette interface constitue la preuve d’intégration applicative du service IA.

## 2. Choix technique retenu

Le choix retenu pour le Bloc 3 est une application frontend légère :

```text
HTML + CSS + JavaScript
Docker
Nginx
API FastAPI existante
```

Ce choix est adapté au projet car :

- il est simple à maintenir ;
- il ne nécessite pas de framework frontend lourd ;
- il permet une démonstration rapide ;
- il s’intègre facilement avec Docker Compose ;
- il consomme directement les routes de l’API IA ;
- il couvre les besoins du Bloc 3 sans complexifier inutilement l’architecture.

Un framework comme React ou Vue aurait pu être envisagé, mais il aurait ajouté de la complexité pour une preuve de concept. L’objectif du Bloc 3 est surtout de démontrer l’intégration d’un service IA dans une application utilisable.

## 3. Structure réelle des fichiers

La structure frontend mise en place est la suivante :

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

Cette structure est volontairement simple.

| Fichier | Rôle |
|---|---|
| `frontend/index.html` | Structure de la page web |
| `frontend/css/styles.css` | Mise en forme, responsive et lisibilité |
| `frontend/js/app.js` | Appels API, gestion de la clé API et affichage des résultats |
| `frontend/nginx.conf` | Configuration Nginx et proxy vers l’API FastAPI |
| `frontend/Dockerfile` | Image Docker du frontend |
| `docker-compose.yml` | Orchestration du frontend avec l’API, PostgreSQL et pgAdmin |

## 4. Écrans et sections développés

L’application est composée d’une seule page avec plusieurs sections.

| Section | Description |
|---|---|
| En-tête | Nom du projet et contexte Bloc 3 |
| Configuration API | Saisie de l’URL API et de la clé API |
| Test de connexion | Vérification de l’accès à une route IA protégée |
| Prédiction d’intention | Saisie d’un commentaire et appel du modèle IA |
| Résultat IA | Affichage de l’intention, confiance, temps de réponse et version modèle |
| Informations modèle | Affichage des métadonnées du modèle IA |
| Métriques modèle | Affichage des métriques d’évaluation |
| Monitoring IA | Accès au dashboard HTML et aux alertes CSV |
| Messages utilisateur | Affichage des succès, erreurs et avertissements |

La prédiction batch n’a pas été intégrée dans l’interface actuelle. Elle reste disponible côté API, mais n’est pas prioritaire pour cette première version frontend.

## 5. Fonctionnalités implémentées

## 5.1. Configuration API

L’utilisateur peut configurer :

```text
URL de base de l’API IA ;
clé API utilisée pour les routes protégées.
```

La configuration est stockée côté navigateur avec `localStorage` afin de faciliter les tests successifs.

Champs utilisés :

```text
apiBaseUrl
apiKey
```

Valeurs par défaut en environnement Docker local :

```text
URL API : /api/v1/ai
Clé API : paylive-dev-api-key
```

Le frontend utilise une URL relative car Nginx sert de proxy vers l’API FastAPI.

## 5.2. Test sécurisé de connexion

Le bouton de test de connexion vérifie maintenant une route protégée :

```text
GET /api/v1/ai/model-info
```

Ce choix permet de vérifier deux choses :

```text
l’API est disponible ;
la clé API est valide.
```

Cas gérés :

| Cas | Résultat affiché |
|---|---|
| Clé API correcte | API IA disponible et clé API valide |
| Clé API absente | Erreur de clé API |
| Clé API invalide | Erreur “Clé API invalide” |
| API indisponible | Message d’erreur de connexion |

Cette correction est importante car la route `/health` est publique et ne permet pas de vérifier réellement l’authentification.

## 5.3. Prédiction d’intention

L’utilisateur saisit un commentaire de live shopping, par exemple :

```text
je prends la robe noire en M
```

Le frontend appelle la route :

```text
POST /api/v1/ai/predict-intent
```

Payload envoyé :

```json
{
  "comment_text": "je prends la robe noire en M"
}
```

Header envoyé :

```text
X-API-Key: paylive-dev-api-key
```

La réponse est ensuite traitée par JavaScript et affichée dans l’interface.

## 5.4. Affichage du résultat IA

Les informations affichées sont :

| Donnée | Description |
|---|---|
| `predicted_intent` | Intention prédite par le modèle |
| `confidence_score` | Score de confiance |
| `response_time_ms` | Temps de réponse du modèle |
| `model_version` | Version du modèle utilisé |
| `is_low_confidence` | Indicateur de confiance faible |

Si la prédiction est à faible confiance, un message d’avertissement est affiché :

```text
Attention : le score de confiance est faible. Une validation humaine est recommandée.
```

Cette règle est cohérente avec le monitoring du Bloc 2.

## 5.5. Informations modèle

Le bouton **Charger les informations** appelle :

```text
GET /api/v1/ai/model-info
```

L’objectif est de rendre visibles les métadonnées du modèle IA :

```text
type de modèle ;
version ;
chemin des artefacts ;
classes connues ;
date ou informations d’entraînement selon les métadonnées disponibles.
```

La réponse JSON est affichée dans un bloc lisible.

## 5.6. Métriques modèle

Le bouton **Charger les métriques** appelle :

```text
GET /api/v1/ai/model-metrics
```

L’objectif est de consulter les résultats d’évaluation du modèle :

```text
accuracy ;
macro F1 ;
weighted F1 ;
rapport de classification ;
informations du benchmark si disponibles.
```

La réponse est affichée au format JSON dans l’interface.

## 5.7. Monitoring IA

La section monitoring donne accès à deux fonctionnalités :

```text
ouvrir le dashboard HTML de monitoring ;
télécharger les alertes CSV.
```

Routes utilisées :

```text
GET /api/v1/ai/monitoring/dashboard
GET /api/v1/ai/monitoring/alerts
```

Le dashboard est ouvert dans un nouvel onglet à partir du contenu HTML retourné par l’API.

Le fichier d’alertes est téléchargé côté navigateur sous le nom :

```text
model_monitoring_alerts.csv
```

## 6. Gestion des appels API

Le fichier `frontend/js/app.js` centralise la configuration et les appels API.

Fonctions principales :

| Fonction | Rôle |
|---|---|
| `getHeaders()` | Préparer les headers avec `Content-Type` et `X-API-Key` |
| `getApiBaseUrl()` | Récupérer l’URL API configurée |
| `formatJson()` | Afficher proprement les réponses JSON |
| `showError()` | Afficher les erreurs utilisateur |
| événement `predictBtn` | Appeler la prédiction d’intention |
| événement `modelInfoBtn` | Charger les informations modèle |
| événement `modelMetricsBtn` | Charger les métriques modèle |
| événement `openDashboardBtn` | Ouvrir le dashboard monitoring |
| événement `downloadAlertsBtn` | Télécharger les alertes CSV |

Tous les appels protégés envoient le header :

```javascript
"X-API-Key": apiKeyInput.value.trim()
```

## 7. Gestion des erreurs

L’application gère plusieurs types d’erreurs :

| Erreur | Gestion prévue |
|---|---|
| Commentaire vide | Message demandant de saisir un commentaire |
| Clé API invalide | Message d’erreur explicite |
| API indisponible | Message de connexion refusée |
| Route protégée refusée | Erreur HTTP affichée |
| Réponse non OK | Message avec le code HTTP |

Une correction importante a été apportée au test de connexion : il ne teste plus uniquement `/health`, car cette route est publique. Il teste désormais une route protégée afin de valider réellement la clé API.

## 8. Accessibilité intégrée

L’interface intègre des bonnes pratiques d’accessibilité de base :

```text
lang="fr" ;
balise main ;
labels associés aux champs ;
boutons HTML natifs ;
messages avec aria-live ;
textes d’erreur explicites ;
contrastes lisibles ;
interface responsive ;
information non transmise uniquement par couleur.
```

Les champs principaux sont associés à des labels :

```text
apiBaseUrl
apiKey
commentText
```

Les zones dynamiques utilisent `aria-live="polite"` pour informer l’utilisateur des changements.

## 9. Responsive design et correction de mise en page

Une correction CSS a été appliquée pour éviter que les sections **Informations modèle** et **Métriques modèle** soient affichées côte à côte avec des contenus JSON trop larges.

La classe `.grid-2` utilise désormais une seule colonne :

```css
.grid-2 {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}
```

Le bloc JSON a également été rendu plus robuste :

```css
.json-output {
  overflow: auto;
  max-height: 420px;
  white-space: pre-wrap;
  word-break: break-word;
}
```

Ces corrections améliorent :

```text
la lisibilité ;
l’ergonomie ;
la compatibilité avec les petits écrans ;
la présentation en soutenance.
```

## 10. Dockerisation du frontend

Le frontend est servi par Nginx.

Fichier :

```text
frontend/Dockerfile
```

Contenu fonctionnel :

```dockerfile
FROM nginx:1.27-alpine

COPY index.html /usr/share/nginx/html/index.html
COPY css /usr/share/nginx/html/css
COPY js /usr/share/nginx/html/js
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

Ce conteneur sert les fichiers statiques de l’application.

## 11. Configuration Nginx

Le fichier `frontend/nginx.conf` sert l’application et redirige les appels vers l’API FastAPI.

Routes proxy principales :

```text
/health  -> http://api:8000/health
/api/    -> http://api:8000/api/
```

Cette configuration permet au frontend d’utiliser des URLs relatives comme :

```text
/api/v1/ai/predict-intent
/api/v1/ai/model-info
```

Avantages :

- pas besoin d’exposer directement l’URL interne du conteneur API au navigateur ;
- pas de problème CORS dans l’usage Docker local ;
- architecture cohérente avec Docker Compose.

## 12. Intégration dans Docker Compose

Le service frontend est ajouté dans `docker-compose.yml` :

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

Services attendus dans l’environnement local :

```text
paylive_postgres
paylive_pgadmin
paylive_api
paylive_frontend
```

## 13. Commandes de développement

Construire et lancer toute la stack :

```bash
docker compose up -d --build
```

Construire uniquement le frontend :

```bash
docker compose up -d --build frontend
```

Vérifier les conteneurs :

```bash
docker compose ps
```

Voir les logs frontend :

```bash
docker logs --tail 80 paylive_frontend
```

Voir les logs API :

```bash
docker logs --tail 80 paylive_api
```

Accéder à l’application :

```text
http://127.0.0.1:8080
```

Accéder à l’API :

```text
http://127.0.0.1:8000/docs
```

## 14. Flux utilisateur principal

Le parcours principal est le suivant :

```text
1. l’utilisateur ouvre http://127.0.0.1:8080 ;
2. il vérifie ou renseigne l’URL API et la clé API ;
3. il teste la connexion sécurisée ;
4. il saisit un commentaire de live ;
5. il clique sur “Analyser le commentaire” ;
6. le frontend appelle l’API IA ;
7. l’API retourne l’intention prédite ;
8. le frontend affiche le résultat ;
9. si la confiance est faible, une alerte est affichée ;
10. l’utilisateur peut consulter les métriques, le dashboard et les alertes.
```

## 15. Preuves à produire

Captures d’écran recommandées :

```text
interface chargée sur http://127.0.0.1:8080 ;
test de connexion avec clé API valide ;
test de connexion avec clé API invalide ;
saisie d’un commentaire ;
résultat de prédiction affiché ;
message de faible confiance si applicable ;
informations modèle affichées ;
métriques modèle affichées ;
dashboard monitoring ouvert depuis le frontend ;
alertes CSV téléchargées ;
docker compose ps avec paylive_frontend actif ;
GitHub Actions en vert.
```

## 16. Commit réalisé ou prévu

Commit recommandé pour l’interface :

```bash
git add frontend
git add docker-compose.yml
git commit -m "Add Dockerized HTML JS application for Bloc 3"
```

Commit recommandé pour les corrections UI et clé API :

```bash
git add frontend/css/styles.css
git add frontend/js/app.js
git commit -m "Fix frontend layout and API key validation"
```

## 17. Conclusion

Le développement de l’interface HTML/CSS/JavaScript permet de démontrer l’intégration concrète du service IA dans une application.

La solution reste volontairement légère, mais elle couvre les besoins essentiels du Bloc 3 :

```text
saisie utilisateur ;
appel API sécurisé ;
traitement de la réponse IA ;
affichage du résultat ;
gestion des erreurs ;
monitoring ;
dashboard ;
alertes ;
conteneurisation Docker ;
intégration dans Docker Compose.
```

Cette interface constitue une preuve applicative claire pour la soutenance du dossier professionnel.
