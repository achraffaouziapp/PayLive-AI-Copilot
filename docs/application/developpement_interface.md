# Développement de l’interface — Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document décrit le plan de développement de l’interface web HTML/CSS/JavaScript du Bloc 3.

L’objectif est de construire une interface simple, conteneurisée avec Docker, capable de consommer l’API IA existante.

## 2. Structure de fichiers à créer

La structure cible est la suivante :

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

## 3. Rôle des fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | Structure HTML de l’application |
| `styles.css` | Mise en forme, accessibilité, responsive |
| `config.js` | Configuration des routes API |
| `app.js` | Logique d’appel API et affichage des résultats |
| `Dockerfile` | Image Docker du frontend |
| `nginx.conf` | Configuration Nginx pour servir l’application |

## 4. Écrans à développer

L’application sera composée d’une seule page avec plusieurs sections.

| Section | Description |
|---|---|
| En-tête | Nom du projet et statut API |
| Configuration | Saisie de la clé API et URL API |
| Prédiction simple | Formulaire commentaire unique |
| Résultat IA | Carte de résultat avec intention et confiance |
| Prédiction batch | Zone de saisie multi-commentaires |
| Tableau batch | Résultats de plusieurs prédictions |
| Modèle | Informations et métriques du modèle |
| Monitoring | Accès dashboard et alertes |
| Erreurs | Zone centralisée pour les messages d’erreur |

## 5. Variables de configuration

Le fichier `config.js` contiendra :

```javascript
window.PAYLIVE_CONFIG = {
  API_BASE_URL: "http://127.0.0.1:8000",
  DEFAULT_API_KEY: "paylive-dev-api-key",
  LOW_CONFIDENCE_THRESHOLD: 0.60,
  ENDPOINTS: {
    health: "/health",
    predictIntent: "/api/v1/ai/predict-intent",
    batchPredictIntents: "/api/v1/ai/batch-predict-intents",
    modelInfo: "/api/v1/ai/model-info",
    modelMetrics: "/api/v1/ai/model-metrics",
    monitoringDashboard: "/api/v1/ai/monitoring/dashboard",
    monitoringAlerts: "/api/v1/ai/monitoring/alerts"
  }
};
```

Pour une version production, la clé API ne doit pas être préremplie dans le code.

Dans ce projet, la valeur par défaut sert uniquement à faciliter la démonstration locale.

## 6. Fonctions JavaScript principales

Le fichier `app.js` contiendra les fonctions suivantes :

| Fonction | Rôle |
|---|---|
| `getApiKey()` | Récupérer la clé API saisie |
| `getApiBaseUrl()` | Récupérer l’URL de l’API |
| `apiFetch(endpoint, options)` | Centraliser les appels API |
| `checkApiHealth()` | Tester l’état du backend |
| `predictSingleComment()` | Appeler la prédiction simple |
| `predictBatchComments()` | Appeler la prédiction batch |
| `loadModelInfo()` | Charger les informations du modèle |
| `loadModelMetrics()` | Charger les métriques |
| `openMonitoringDashboard()` | Charger ou ouvrir le dashboard |
| `downloadAlerts()` | Télécharger les alertes CSV |
| `showError(message)` | Afficher une erreur accessible |
| `showSuccess(message)` | Afficher un message de succès |
| `renderPrediction(prediction)` | Afficher un résultat IA |
| `renderBatchResults(predictions)` | Afficher un tableau de résultats |

## 7. Gestion des appels API

Tous les appels API protégés doivent envoyer :

```javascript
headers: {
  "Content-Type": "application/json",
  "X-API-Key": apiKey
}
```

Exemple de logique :

```javascript
async function apiFetch(endpoint, options = {}) {
  const apiBaseUrl = getApiBaseUrl();
  const apiKey = getApiKey();

  const response = await fetch(`${apiBaseUrl}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": apiKey,
      ...(options.headers || {})
    }
  });

  if (!response.ok) {
    throw new Error(`Erreur API ${response.status}`);
  }

  return response;
}
```

## 8. Affichage des prédictions

Le résultat d’une prédiction simple doit être affiché sous forme de carte.

Champs attendus :

```text
comment_text
predicted_intent
predicted_intent_label
confidence_score
is_low_confidence
response_time_ms
model_version
```

Affichage métier recommandé :

| Valeur technique | Libellé interface |
|---|---|
| `purchase_intent` | Intention d’achat |
| `product_question` | Question produit |
| `payment_question` | Question paiement |
| `shipping_question` | Question livraison |
| `other` | Autre message |
| `unknown` | Intention inconnue |

## 9. Gestion des états UI

L’interface doit gérer plusieurs états :

| État | Comportement |
|---|---|
| Chargement | Bouton désactivé + message “Analyse en cours” |
| Succès | Résultat affiché |
| Erreur | Message d’erreur dans une zone dédiée |
| Faible confiance | Alerte visuelle et textuelle |
| API indisponible | Message “backend inaccessible” |

## 10. Accessibilité à intégrer dans le code

Dans `index.html` :

- utiliser `lang="fr"` ;
- utiliser une balise `<main>` ;
- associer les champs à des `<label>` ;
- utiliser des boutons `<button>` ;
- prévoir une zone `aria-live="polite"` pour les résultats ;
- prévoir une zone `aria-live="assertive"` pour les erreurs.

Dans `styles.css` :

- définir un style visible pour `:focus` ;
- garantir une taille de police lisible ;
- ne pas transmettre l’information uniquement par couleur ;
- prévoir une mise en page responsive.

Dans `app.js` :

- ne pas supprimer brutalement les messages d’erreur ;
- mettre à jour les zones live ;
- afficher des messages textuels explicites.

## 11. Dockerisation du frontend

### Dockerfile

```dockerfile
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY public /usr/share/nginx/html

EXPOSE 80
```

### nginx.conf

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

### docker-compose.yml

Ajouter le service suivant :

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

## 12. Configuration CORS côté API

L’API devra autoriser le frontend :

```text
http://localhost:8080
http://127.0.0.1:8080
```

Dans `api/main.py`, ajouter ou vérifier :

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

## 13. Commandes de développement

Construire et lancer les services :

```bash
docker compose up -d --build
```

Vérifier les conteneurs :

```bash
docker compose ps
```

Accéder au frontend :

```text
http://localhost:8080
```

Accéder à l’API :

```text
http://localhost:8000/docs
```

Voir les logs frontend :

```bash
docker logs --tail 80 paylive_frontend
```

Voir les logs API :

```bash
docker logs --tail 80 paylive_api
```

## 14. Preuves à produire

Captures d’écran recommandées :

```text
interface chargée sur localhost:8080
saisie d’un commentaire
résultat purchase_intent affiché
alerte faible confiance affichée
analyse batch affichée
infos modèle affichées
métriques modèle affichées
dashboard monitoring ouvert depuis le front
alertes CSV téléchargées ou affichées
docker compose ps avec frontend et api actifs
```

## 15. Commit prévu

Quand l’interface fonctionnera :

```bash
git add frontend
git add docker-compose.yml
git add api/main.py
git add docs/08_application

git commit -m "Add Dockerized frontend for AI application"
```

## 16. Conclusion

Le développement de l’interface HTML/CSS/JS permet de démontrer concrètement l’intégration du service IA dans une application.

La solution est volontairement simple, mais elle couvre les besoins essentiels : saisie utilisateur, appel API, authentification, traitement de la réponse, affichage du résultat, gestion des erreurs, monitoring et conteneurisation.
