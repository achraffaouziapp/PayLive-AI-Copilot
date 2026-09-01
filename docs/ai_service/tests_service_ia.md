# Tests automatisés et stratégie de validation du service IA

## 1. Objectif du document

Ce document décrit les tests automatisés mis en place pour valider le service IA et formalise la stratégie de tests associée.

L'objectif est de vérifier la qualité du dataset IA, le chargement du modèle, le fonctionnement des prédictions, la sécurité des routes API IA, la présence des routes dans OpenAPI, l'intégration frontend/API, le monitoring et la couverture réelle du code.

La stratégie couvre la chaîne suivante :

```text
préparation des données
        ↓
entraînement
        ↓
évaluation
        ↓
inférence
        ↓
API
        ↓
frontend / E2E
        ↓
monitoring
```

Pour chaque niveau de test, les éléments suivants sont documentés :

- niveau de test ;
- objectif ;
- donnée testée ;
- résultat attendu ;
- couverture ou preuve associée.

---

## 2. Fichiers de tests

Les tests IA sont organisés dans :

```text
tests/test_ai_dataset.py
tests/test_intent_model.py
tests/test_ai_api.py
tests/e2e/test_frontend_ai.py
```

| Fichier | Rôle |
|---|---|
| `test_ai_dataset.py` | validation du dataset NLP |
| `test_intent_model.py` | validation du modèle et de l'inférence |
| `test_ai_api.py` | validation des routes API IA |
| `test_frontend_ai.py` | tests E2E frontend → API → IA avec Playwright |

Les scripts de la chaîne IA concernés sont notamment :

```text
src/ai/data_preparation/prepare_nlp_dataset.py
src/ai/training/train_intent_classifier.py
src/ai/training/benchmark_intent_models.py
src/ai/inference/intent_predictor.py
src/ai/monitoring/monitor_predictions.py
src/ai/monitoring/generate_monitoring_dashboard.py
api/ai_service.py
api/routes/ai.py
```

---

## 3. Matrice de stratégie de tests

| Niveau de test | Objectif | Donnée testée | Résultat attendu | Couverture / preuve |
|---|---|---|---|---|
| Tests de données | vérifier la qualité et la structure du dataset NLP | fichiers train, validation, test, labels, rapports de préparation | dataset lisible, classes présentes, structure conforme | `tests/test_ai_dataset.py` |
| Tests unitaires du modèle | vérifier le chargement et le comportement du classifieur | commentaires simulés + artefacts du modèle | intention valide, score de confiance, modèle chargé | `tests/test_intent_model.py` |
| Tests d'inférence | vérifier texte → prédiction | commentaires courts simulés | intention, confiance, version et temps de réponse retournés | `intent_predictor.py` + tests modèle/API |
| Tests API IA | vérifier l'exposition FastAPI et la sécurité | requêtes HTTP, clés API, payloads JSON | statuts HTTP et réponses conformes | `tests/test_ai_api.py` |
| Tests E2E | vérifier l'intégration réelle de l'application | actions Chromium sur l'interface | frontend → Nginx → API → IA fonctionnel | `tests/e2e/test_frontend_ai.py` |
| Tests monitoring | vérifier logs, métriques, dashboard et alertes | prédictions simulées | monitoring recalculable et consultable | procédure C11 |
| Tests entraînement/évaluation | vérifier la reproductibilité ML | datasets train/validation/test | artefacts + métriques générés | scripts training/benchmark |
| Couverture de code | mesurer les lignes exécutées par les tests | `src/ai` + `api` | rapport terminal + HTML | `pytest-cov` / `coverage.py` |

---

## 4. Tests du dataset IA

Fichier :

```text
tests/test_ai_dataset.py
```

Objectifs :

- vérifier que les fichiers dataset existent ;
- vérifier que les rapports de préparation existent ;
- vérifier que le dataset complet n'est pas vide ;
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

### Niveau de test

```text
Test de données / validation de dataset
```

### Donnée testée

Les fichiers NLP préparés et leurs rapports de qualité.

### Résultat attendu

Les datasets doivent être lisibles, non vides, cohérents et compatibles avec la chaîne d'entraînement.

### Couverture

La qualité fonctionnelle du dataset est couverte par `tests/test_ai_dataset.py`. La couverture Python ne mesure pas directement la qualité des données : elle doit être interprétée avec les assertions fonctionnelles.

---

## 5. Tests du modèle IA

Fichier :

```text
tests/test_intent_model.py
```

Objectifs :

- vérifier que les artefacts du modèle existent ;
- vérifier que les rapports d'entraînement existent ;
- vérifier que le modèle peut être chargé ;
- vérifier qu'une prédiction simple retourne le bon format ;
- vérifier qu'un commentaire d'achat clair est classé en `purchase_intent` ;
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

### Niveau de test

```text
Test unitaire / test fonctionnel du modèle
```

### Donnée testée

Commentaires simulés, artefacts du modèle et métadonnées.

### Résultat attendu

Une prédiction doit contenir des informations cohérentes :

```text
predicted_intent
confidence_score
response_time_ms
model_version
```

### Couverture réelle observée

```text
src/ai/inference/intent_predictor.py → 85 %
```

---

## 6. Tests de l'API IA

Fichier :

```text
tests/test_ai_api.py
```

Objectifs :

- vérifier qu'un appel sans clé API retourne 401 ;
- vérifier qu'un appel avec mauvaise clé API retourne 403 ;
- vérifier qu'un appel avec clé valide retourne une prédiction ;
- vérifier qu'un commentaire vide retourne 400 ;
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

### Niveau de test

```text
Test d'intégration API
```

### Donnée testée

Requêtes HTTP, commentaires simulés, payloads JSON et clés API.

### Résultat attendu

| Cas | Résultat attendu |
|---|---:|
| pas de clé API | 401 |
| mauvaise clé API | 403 |
| bonne clé API | 200 |

### Couverture réelle observée

| Module | Couverture |
|---|---:|
| `api/ai_service.py` | 96 % |
| `api/main.py` | 93 % |
| `api/routes/ai.py` | 67 % |
| `api/schemas.py` | 100 % |
| `api/security.py` | 48 % |

---

## 7. Validation du format des réponses

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

Le résultat attendu est une réponse structurée, exploitable par le frontend et le système de monitoring.

---

## 8. Validation OpenAPI

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

---

## 9. Tests sans serveur externe

Les tests API utilisent `TestClient` de FastAPI.

Le fichier `tests/test_ai_api.py` importe directement :

```python
from api.main import app
```

Puis crée :

```python
client = TestClient(app)
```

Cela permet de tester les routes API sans lancer manuellement Uvicorn ou Docker.

---

## 10. Tests E2E frontend / API IA

Fichier :

```text
tests/e2e/test_frontend_ai.py
```

### Niveau de test

```text
Test End-to-End avec Playwright / Chromium
```

### Objectif

Vérifier la chaîne réelle :

```text
Chromium
→ frontend HTML/JavaScript
→ Nginx
→ FastAPI
→ service IA
→ modèle
```

### Donnée testée

Commentaires simulés, clé API valide/invalide et interactions utilisateur réelles.

### Résultat attendu

Les endpoints réellement exploités par le frontend doivent répondre correctement.

Tests exécutés :

```text
test_protected_connection_with_valid_api_key
test_invalid_api_key_is_rejected
test_predict_intent_from_frontend
test_model_info_from_frontend
test_model_metrics_from_frontend
test_monitoring_dashboard_from_frontend
test_monitoring_alerts_from_frontend
```

Résultat obtenu :

```text
7 passed
```

### Couverture

Ces tests apportent une couverture fonctionnelle des endpoints réellement consommés par l'interface, complémentaire au pourcentage de couverture de code.

---

## 11. Tests du monitoring

### Niveau de test

```text
Test d'intégration / validation opérationnelle
```

### Objectif

Vérifier que les prédictions sont journalisées et que les métriques, rapports, dashboard et alertes peuvent être recalculés.

### Donnée testée

Prédictions simulées et fichiers :

```text
data/ai/predictions/ai_predictions_log.csv
data/ai/reports/model_monitoring_report.csv
data/ai/reports/model_monitoring_dashboard.html
data/ai/reports/model_monitoring_alerts.csv
```

### Résultat attendu

Après de nouvelles prédictions :

- les logs évoluent ;
- les métriques sont recalculées ;
- le dashboard est régénérable ;
- les alertes sont recalculées ;
- les résultats sont consultables sous forme graphique et tabulaire.

### Couverture observée

| Module | Couverture |
|---|---:|
| `src/ai/monitoring/monitor_predictions.py` | 44 % |
| `src/ai/monitoring/generate_monitoring_dashboard.py` | 18 % |

---

## 12. Tests d'entraînement et d'évaluation

### Niveau de test

```text
Test de reproductibilité / validation du pipeline ML
```

### Objectif

Vérifier que le modèle peut être réentraîné et évalué à partir du dataset préparé.

### Donnée testée

```text
train.csv
validation.csv
test.csv
```

Scripts :

```text
src/ai/training/train_intent_classifier.py
src/ai/training/benchmark_intent_models.py
```

### Résultat attendu

L'entraînement doit produire :

```text
model.joblib
vectorizer.joblib
label_encoder.joblib
model_metadata.json
```

Le benchmark doit calculer les métriques et permettre de sélectionner le modèle retenu.

### Résultats déjà obtenus

```text
TF-IDF + Logistic Regression

validation_accuracy    = 0.8
validation_macro_f1    = 0.6667
validation_weighted_f1 = 0.7333
```

### Couverture observée

```text
src/ai/training/train_intent_classifier.py  → 0 %
src/ai/training/benchmark_intent_models.py  → 0 %
```

Ces scripts ont été exécutés dans le pipeline du projet, mais ne sont pas directement appelés par la suite Pytest utilisée pour calculer la couverture.

---

## 13. Rapports de tests générés

Les tests génèrent des rapports CSV :

```text
data/ai/reports/ai_dataset_test_report.csv
data/ai/reports/intent_model_test_report.csv
data/ai/reports/ai_api_test_report.csv
```

Ces fichiers servent de preuve d'exécution.

---

## 14. Commandes d'exécution

Avant les tests, il est possible de régénérer les données et le modèle :

```cmd
python src\ai\data_preparation\prepare_nlp_dataset.py
python src\ai\training\train_intent_classifier.py
python src\ai\training\benchmark_intent_models.py
```

Tests séparés :

```cmd
pytest tests\test_ai_dataset.py -v
pytest tests\test_intent_model.py -v
pytest tests\test_ai_api.py -v
```

Exécution groupée :

```cmd
pytest tests\test_ai_dataset.py tests\test_intent_model.py tests\test_ai_api.py -v
```

---

## 15. Mesure de couverture avec pytest-cov

### Installation

```cmd
python -m pip install pytest-cov
```

### Commande utilisée

```cmd
pytest tests\test_ai_dataset.py tests\test_intent_model.py tests\test_ai_api.py -v --cov=src.ai --cov=api --cov-report=term-missing --cov-report=html:htmlcov
```

Variante possible :

```cmd
pytest tests\test_ai_dataset.py tests\test_intent_model.py tests\test_ai_api.py -v --cov=src/ai --cov=api --cov-report=term-missing --cov-report=html:htmlcov
```

### Rapport HTML

```cmd
start htmlcov\index.html
```

Le rapport HTML permet d'identifier les fichiers couverts, les lignes exécutées, les lignes manquantes et le taux global.

---

## 16. Résultat réel de couverture

Mesure réalisée le **1er septembre 2026 à 22:14** :

```text
Couverture globale : 32 %
Statements          : 1442
Missing             : 982
Excluded            : 0
```

Outil :

```text
coverage.py 7.16.0
```

### Modules les mieux couverts

| Module | Couverture |
|---|---:|
| `api/schemas.py` | 100 % |
| `api/ai_service.py` | 96 % |
| `api/main.py` | 93 % |
| `src/ai/inference/intent_predictor.py` | 85 % |
| `api/routes/ai.py` | 67 % |

### Modules partiellement couverts

| Module | Couverture |
|---|---:|
| `api/routes/health.py` | 67 % |
| `api/routes/lives.py` | 53 % |
| `api/routes/sellers.py` | 50 % |
| `api/routes/analytics.py` | 48 % |
| `api/security.py` | 48 % |
| `src/ai/monitoring/monitor_predictions.py` | 44 % |
| `api/database.py` | 33 % |
| `src/ai/monitoring/generate_monitoring_dashboard.py` | 18 % |

### Modules à 0 % dans cette mesure

```text
src/ai/data_preparation/prepare_nlp_dataset.py
src/ai/training/benchmark_intent_models.py
src/ai/training/train_intent_classifier.py
```

---

## 17. Analyse de la couverture

Le taux global de **32 %** est une mesure réelle et traçable. Il montre que la suite Pytest actuelle ne couvre pas encore toute la chaîne Python.

Le taux global est diminué principalement par :

- les scripts de préparation de données non appelés par Pytest ;
- les scripts d'entraînement et benchmark non appelés par Pytest ;
- les branches de monitoring encore peu couvertes ;
- des routes métier du Bloc 1 incluses dans le périmètre `api`.

En revanche, les composants centraux de l'inférence et du service IA sont nettement mieux couverts :

```text
api/ai_service.py                 96 %
src/ai/inference/intent_predictor.py 85 %
api/routes/ai.py                  67 %
api/schemas.py                   100 %
```

La couverture est donc analysée avec les autres preuves de qualité :

- tests fonctionnels ;
- métriques d'évaluation ;
- benchmark ;
- tests API ;
- tests E2E ;
- validation du monitoring ;
- workflow CI/MLOps.

---

## 18. Plan d'amélioration

### Priorité 1 — préparation des données

Ajouter des tests sur :

```text
prepare_nlp_dataset.py
```

Objectifs :

- création correcte des splits ;
- contrôle des classes ;
- gestion des doublons ;
- validation des colonnes finales.

### Priorité 2 — entraînement

Rendre les fonctions principales des scripts de training appelables depuis Pytest.

Tests recommandés :

- entraînement sur un petit dataset temporaire ;
- génération des artefacts ;
- calcul des métriques ;
- sélection du modèle ;
- comportement en cas de fichier absent.

### Priorité 3 — monitoring

Ajouter des tests sur :

```text
monitor_predictions.py
generate_monitoring_dashboard.py
```

Tests recommandés :

- log d'une prédiction ;
- log d'un batch ;
- génération du rapport ;
- génération d'une alerte faible confiance ;
- génération du HTML ;
- comportement sans fichier de prédictions.

### Priorité 4 — sécurité API

Compléter les branches :

```text
clé valide
clé absente
clé invalide
```

---

## 19. Intégration continue

La couverture peut être intégrée au workflow GitHub Actions :

```yaml
- name: Run AI tests with coverage
  run: >
    pytest
    tests/test_ai_dataset.py
    tests/test_intent_model.py
    tests/test_ai_api.py
    -v
    --cov=src.ai
    --cov=api
    --cov-report=term-missing
    --cov-report=html:htmlcov
```

Le dossier `htmlcov` peut être conservé comme artefact de CI.

Un seuil minimal pourra être ajouté ultérieurement avec :

```text
--cov-fail-under=<seuil>
```

Aucun seuil artificiel n'est imposé dans le POC tant qu'il n'est pas justifié.

---

## 20. Critères de réussite

La stratégie de tests est considérée comme appliquée lorsque :

- les tests du dataset sont exécutables ;
- les tests du modèle sont exécutables ;
- les tests API sont exécutables ;
- les tests E2E sont exécutables ;
- le monitoring est vérifiable ;
- la couverture est calculée ;
- un rapport HTML est généré ;
- les zones non couvertes sont identifiées ;
- les limites et axes d'amélioration sont documentés.

Une couverture élevée ne constitue pas à elle seule une preuve de qualité : les assertions fonctionnelles et les tests d'intégration restent nécessaires.

---

## 21. Preuves à conserver

Captures recommandées :

```text
preuve_c12_tests_ia_passed.png
preuve_c12_coverage_terminal.png
preuve_c12_coverage_html_global.png
preuve_c12_coverage_intent_predictor.png
preuve_c12_coverage_api_ai_service.png
preuve_c12_tests_e2e_7_passed.png
```

Fichiers à conserver :

```text
tests/test_ai_dataset.py
tests/test_intent_model.py
tests/test_ai_api.py
tests/e2e/test_frontend_ai.py
htmlcov/index.html
docs/ai_service/28_tests_service_ia.md
```

---

## 22. Conclusion

Les tests automatisés valident les principales briques du service IA : dataset, modèle, inférence, API, sécurité, documentation OpenAPI, intégration E2E et monitoring.

La stratégie de tests formalise désormais le niveau de test, l'objectif, les données testées, les résultats attendus et la couverture associée.

La couverture de code est mesurée avec `pytest-cov` et atteint actuellement **32 %** sur le périmètre analysé. Cette valeur met en évidence des zones encore peu couvertes, notamment les scripts de préparation, d'entraînement et certaines fonctions de monitoring, tandis que les composants centraux de l'inférence et du service IA présentent une couverture sensiblement plus élevée.

Cette mesure fournit une base objective pour améliorer progressivement la qualité et la traçabilité du service IA.
