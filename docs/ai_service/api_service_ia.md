# API du service IA — PayLive AI Copilot

## 1. Objectif du document

Ce document décrit l’intégration du modèle d’intelligence artificielle dans l’API REST du projet **PayLive AI Copilot**.

L’objectif est de rendre le modèle de classification d’intentions accessible via des routes API sécurisées.

## 2. Rôle de l’API IA

L’API IA permet :

- de prédire l’intention d’un commentaire ;
- de prédire les intentions de plusieurs commentaires ;
- de consulter les informations du modèle ;
- de consulter les métriques du modèle ;
- d’exposer le service IA dans Swagger / OpenAPI.

## 3. Architecture d’intégration

L’intégration repose sur trois couches :

```text
api/routes/ai.py
        ↓
api/ai_service.py
        ↓
src/ai/inference/intent_predictor.py
        ↓
models/intent_classifier/
```

| Fichier | Rôle |
|---|---|
| api/routes/ai.py | expose les routes FastAPI |
| api/ai_service.py | couche service entre API et modèle |
| src/ai/inference/intent_predictor.py | chargement du modèle et prédiction |
| models/intent_classifier/ | artefacts du modèle entraîné |

## 4. Module d’inférence

Le module d’inférence est :

```text
src/ai/inference/intent_predictor.py
```

Il charge :

```text
models/intent_classifier/model.joblib
models/intent_classifier/vectorizer.joblib
models/intent_classifier/label_encoder.joblib
models/intent_classifier/model_metadata.json
```

Fonctions principales :

```text
load_model_artifacts()
predict_intent(comment_text)
predict_batch(comment_texts)
get_model_info()
get_model_metrics()
```

## 5. Couche service API

La couche service est :

```text
api/ai_service.py
```

Elle permet :

- d’appeler le module d’inférence ;
- d’ajouter un statut de faible confiance ;
- de lire les métriques d’évaluation ;
- de lire le rapport de sélection du benchmark ;
- d’enregistrer les prédictions dans le monitoring.

Seuil de faible confiance :

```text
0.60
```

Si le score de confiance est inférieur à ce seuil, la prédiction est marquée comme incertaine.

## 6. Routes API IA

| Méthode | Route | Description |
|---|---|---|
| POST | /api/v1/ai/predict-intent | prédire une intention pour un commentaire |
| POST | /api/v1/ai/batch-predict-intents | prédire plusieurs intentions |
| GET | /api/v1/ai/model-info | obtenir les informations du modèle |
| GET | /api/v1/ai/model-metrics | obtenir les métriques du modèle |

## 7. Sécurité

Les routes IA sont protégées par la même clé API que le Bloc 1.

Header attendu :

```text
X-API-Key
```

Valeur de développement :

```text
paylive-dev-api-key
```

| Cas | Code HTTP |
|---|---:|
| clé API absente | 401 |
| clé API incorrecte | 403 |
| clé API valide | 200 |

## 8. Route de prédiction simple

Route :

```text
POST /api/v1/ai/predict-intent
```

Exemple de corps JSON :

```json
{
  "comment_text": "je prends la robe noire en M"
}
```

Réponse attendue :

```json
{
  "comment_text": "je prends la robe noire en M",
  "predicted_intent": "purchase_intent",
  "confidence_score": 0.25,
  "model_name": "intent_classifier",
  "model_version": "intent_classifier_v1",
  "response_time_ms": 1200.0,
  "is_low_confidence": true,
  "low_confidence_threshold": 0.6
}
```

Le score peut varier selon l’entraînement.

## 9. Route de prédiction batch

Route :

```text
POST /api/v1/ai/batch-predict-intents
```

Exemple de corps JSON :

```json
{
  "comments": [
    "je prends le pull rouge en M",
    "comment payer ?",
    "vous livrez en Belgique ?",
    "trop beau"
  ]
}
```

La réponse contient un tableau de prédictions détaillées.

## 10. Route d’information modèle

Route :

```text
GET /api/v1/ai/model-info
```

Elle retourne notamment : nom du modèle, version, algorithme, date d’entraînement, classes, chemins des artefacts, sélection benchmark et seuil de faible confiance.

## 11. Route de métriques modèle

Route :

```text
GET /api/v1/ai/model-metrics
```

Elle retourne notamment les métriques du fichier `model_metadata.json`, le rapport d’évaluation, la sélection benchmark et le seuil de faible confiance.

## 12. Documentation Swagger

Les routes IA sont visibles dans Swagger :

```text
http://127.0.0.1:8000/docs
```

La documentation OpenAPI est disponible ici :

```text
http://127.0.0.1:8000/openapi.json
```

## 13. Intégration dans `api/main.py`

Le routeur IA est ajouté dans `api/main.py` :

```python
from api.routes import health, lives, sellers, analytics, ai
```

Puis :

```python
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI service"])
```

## 14. Lancement local avec Uvicorn

```bash
python -m uvicorn api.main:app --reload
```

## 15. Lancement avec Docker

Le service API peut aussi être lancé avec Docker Compose.

```bash
docker compose up -d --build
```

Service attendu :

```text
paylive_api
```

Depuis le navigateur :

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
```

## 16. Test PowerShell — prédiction simple

```powershell
$headers = @{ "X-API-Key" = "paylive-dev-api-key" }

$body = @{
    comment_text = "je prends la robe noire en M"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/ai/predict-intent" `
  -Method POST `
  -Headers $headers `
  -Body $body `
  -ContentType "application/json"
```

## 17. Test PowerShell — informations modèle

```powershell
$headers = @{ "X-API-Key" = "paylive-dev-api-key" }

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/ai/model-info" `
  -Method GET `
  -Headers $headers
```

## 18. Erreur rencontrée et correction

Lors de l’intégration du monitoring, l’API a rencontré une erreur :

```text
ImportError: cannot import name 'log_prediction'
```

Cause : le service API importait une fonction qui n’était pas encore disponible dans le fichier `monitor_predictions.py` ou le conteneur Docker utilisait un ancien état.

Correction : vérification de la présence des fonctions, puis redémarrage ou reconstruction du service API Docker.

Commande utile :

```bash
docker logs -f paylive_api
```

## 19. Emplacements pour captures d’écran

```text
[CAPTURE À AJOUTER]
Swagger montrant la section AI service
```

```text
[CAPTURE À AJOUTER]
Test PowerShell de /api/v1/ai/predict-intent
```

```text
[CAPTURE À AJOUTER]
Docker logs montrant Application startup complete
```

```text
[CAPTURE À AJOUTER]
Route /health fonctionnelle
```

## 20. Conclusion

Le modèle IA est maintenant exposé via l’API REST FastAPI.

Les routes IA sont sécurisées, documentées dans OpenAPI et compatibles avec le monitoring des prédictions.

Cette étape permet d’utiliser le modèle IA comme un vrai service applicatif.
