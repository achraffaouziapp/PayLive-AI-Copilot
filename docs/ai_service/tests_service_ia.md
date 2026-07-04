# Tests automatisés du service IA — PayLive AI Copilot

## 1. Objectif du document

Ce document décrit les tests automatisés mis en place pour valider le service IA du projet **PayLive AI Copilot**.

Les tests permettent de vérifier la qualité du dataset IA, le chargement du modèle, le fonctionnement des prédictions, la sécurité des routes API IA, la présence des routes dans OpenAPI et la génération de rapports de tests.

## 2. Fichiers de tests

Les tests IA sont organisés dans :

```text
tests/test_ai_dataset.py
tests/test_intent_model.py
tests/test_ai_api.py
```

| Fichier | Rôle |
|---|---|
| test_ai_dataset.py | tests du dataset NLP |
| test_intent_model.py | tests du modèle et de l’inférence |
| test_ai_api.py | tests des routes API IA |

## 3. Tests du dataset IA

Fichier :

```text
tests/test_ai_dataset.py
```

Objectifs :

- vérifier que les fichiers dataset existent ;
- vérifier que les rapports de préparation existent ;
- vérifier que le dataset complet n’est pas vide ;
- vérifier que les commentaires ne sont pas vides ;
- vérifier que les labels appartiennent à la liste autorisée ;
- vérifier que toutes les classes attendues sont présentes ;
- vérifier que train + validation + test = dataset complet.

Fichiers vérifiés :

```text
data/ai/datasets/comments_intent_dataset.csv
data/ai/datasets/train.csv
data/ai/datasets/validation.csv
data/ai/datasets/test.csv
data/ai/reports/nlp_dataset_quality_report.csv
data/ai/reports/train_validation_test_split_report.csv
```

## 4. Tests du modèle IA

Fichier :

```text
tests/test_intent_model.py
```

Objectifs :

- vérifier que les artefacts du modèle existent ;
- vérifier que les rapports d’entraînement existent ;
- vérifier que le modèle peut être chargé ;
- vérifier qu’une prédiction simple retourne le bon format ;
- vérifier qu’un commentaire d’achat clair est classé en `purchase_intent` ;
- vérifier que les commentaires vides sont rejetés ;
- vérifier que la prédiction batch fonctionne ;
- vérifier que les informations du modèle sont accessibles ;
- vérifier que les métriques du modèle sont accessibles.

Artefacts vérifiés :

```text
models/intent_classifier/model.joblib
models/intent_classifier/vectorizer.joblib
models/intent_classifier/label_encoder.joblib
models/intent_classifier/model_metadata.json
```

## 5. Tests de l’API IA

Fichier :

```text
tests/test_ai_api.py
```

Objectifs :

- vérifier qu’un appel sans clé API retourne 401 ;
- vérifier qu’un appel avec mauvaise clé API retourne 403 ;
- vérifier qu’un appel avec clé valide retourne une prédiction ;
- vérifier qu’un commentaire vide retourne 400 ;
- vérifier que la prédiction batch fonctionne ;
- vérifier que la route `model-info` fonctionne ;
- vérifier que la route `model-metrics` fonctionne ;
- vérifier que les routes IA sont présentes dans OpenAPI.

Routes testées :

```text
POST /api/v1/ai/predict-intent
POST /api/v1/ai/batch-predict-intents
GET  /api/v1/ai/model-info
GET  /api/v1/ai/model-metrics
GET  /openapi.json
```

## 6. Rapports de tests générés

Les tests génèrent des rapports CSV :

```text
data/ai/reports/ai_dataset_test_report.csv
data/ai/reports/intent_model_test_report.csv
data/ai/reports/ai_api_test_report.csv
```

Ces rapports servent de preuve d’exécution dans le dossier professionnel.

## 7. Commandes d’exécution

Avant les tests, il est recommandé de régénérer les données IA :

```bash
python src/ai/data_preparation/prepare_nlp_dataset.py
python src/ai/training/train_intent_classifier.py
python src/ai/training/benchmark_intent_models.py
```

Puis lancer les tests :

```bash
pytest tests/test_ai_dataset.py -v
pytest tests/test_intent_model.py -v
pytest tests/test_ai_api.py -v
```

Ou en une seule commande :

```bash
pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py -v
```

## 8. Résultat attendu

Résultat attendu :

```text
passed
```

sur tous les tests.

Les tests doivent également générer les trois rapports CSV.

## 9. Tests sans serveur externe

Les tests API utilisent `TestClient` de FastAPI.

Cela permet de tester l’API sans lancer manuellement Uvicorn ou Docker.

Le fichier `tests/test_ai_api.py` importe directement :

```python
from api.main import app
```

Puis crée :

```python
client = TestClient(app)
```

## 10. Sécurité testée

La sécurité par clé API est testée explicitement.

| Cas | Résultat attendu |
|---|---:|
| pas de clé API | 401 |
| mauvaise clé API | 403 |
| bonne clé API | 200 |

Header utilisé :

```text
X-API-Key
```

## 11. Validation du format des réponses

Les tests vérifient que la réponse de prédiction contient :

```text
comment_text
predicted_intent
confidence_score
model_name
model_version
response_time_ms
is_low_confidence
low_confidence_threshold
```

## 12. Validation OpenAPI

Le test OpenAPI vérifie la présence des routes IA dans :

```text
/openapi.json
```

Routes attendues :

```text
/api/v1/ai/predict-intent
/api/v1/ai/batch-predict-intents
/api/v1/ai/model-info
/api/v1/ai/model-metrics
```

## 13. Emplacements pour captures d’écran

```text
[CAPTURE À AJOUTER]
Terminal montrant les tests IA passés avec pytest
```

```text
[CAPTURE À AJOUTER]
Dossier data/ai/reports avec les rapports de tests générés
```

```text
[CAPTURE À AJOUTER]
Extrait de ai_api_test_report.csv
```

## 14. Conclusion

Les tests automatisés valident les principales briques du service IA : dataset, modèle, inférence, API, sécurité et documentation OpenAPI.

Cette étape renforce la fiabilité du Bloc 2 et fournit des preuves techniques exploitables dans le dossier final.
