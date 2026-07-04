# Spécifications techniques du service IA — PayLive AI Copilot

## 1. Objectif du document

Ce document présente les spécifications techniques du service d’intelligence artificielle du projet **PayLive AI Copilot**.

Le Bloc 2 du projet consiste à intégrer un service IA capable d’analyser les commentaires issus de lives de vente et de prédire l’intention exprimée par l’utilisateur.

Le service IA doit être :

- entraînable localement ;
- sauvegardé sous forme d’artefacts réutilisables ;
- exposé via une API REST ;
- sécurisé avec une clé API ;
- testé automatiquement ;
- monitoré à travers des rapports et des logs.

## 2. Rappel du besoin fonctionnel

Pendant un live shopping, les spectateurs peuvent envoyer de nombreux commentaires.

Ces commentaires peuvent correspondre à plusieurs intentions :

- achat ;
- question produit ;
- question livraison ;
- question paiement ;
- commentaire général ;
- commentaire ambigu ou inconnu.

L’objectif du service IA est de classifier automatiquement ces commentaires afin d’aider le vendeur à identifier plus rapidement les messages à forte valeur commerciale.

Exemple :

```text
je prends le pull rouge en M
```

Résultat attendu :

```text
purchase_intent
```

## 3. Problème IA traité

Le problème traité est un problème de :

```text
classification supervisée de texte
```

Le modèle reçoit un texte en entrée et prédit une classe d’intention.

Entrée :

```json
{
  "comment_text": "je prends le pull rouge en M"
}
```

Sortie :

```json
{
  "comment_text": "je prends le pull rouge en M",
  "predicted_intent": "purchase_intent",
  "confidence_score": 0.91,
  "model_version": "intent_classifier_v1"
}
```

## 4. Architecture générale du service IA

Le service IA s’intègre à l’architecture existante du projet.

```text
data/processed/clean/live_comments_clean.csv
        ↓
préparation du dataset NLP
        ↓
contrôle qualité du dataset NLP
        ↓
séparation train / validation / test
        ↓
entraînement du modèle IA
        ↓
évaluation du modèle
        ↓
benchmark de plusieurs approches
        ↓
sauvegarde des artefacts modèle
        ↓
chargement du modèle dans FastAPI
        ↓
exposition via routes API IA
        ↓
tests automatisés
        ↓
monitoring des prédictions
```

## 5. Données en entrée

Le service IA s’appuie sur les données nettoyées produites dans le Bloc 1.

Fichier source principal :

```text
data/processed/clean/live_comments_clean.csv
```

Colonnes utilisées :

| Colonne | Rôle |
|---|---|
| comment_id | identifiant unique du commentaire |
| live_id | identifiant du live |
| customer_id | identifiant pseudonymisé de l’utilisateur |
| platform | plateforme du commentaire |
| username | nom utilisateur simulé ou pseudonymisé |
| comment_text | texte à analyser |
| commented_at | date du commentaire |
| comment_language | langue du commentaire |
| manual_intent_label | label cible |
| extracted_product_keyword | mot-clé produit potentiel |
| data_quality_status | statut qualité |

Colonne d’entrée du modèle :

```text
comment_text
```

Colonne cible :

```text
manual_intent_label
```

## 6. Classes du modèle

Le modèle doit prédire une des classes suivantes :

| Classe | Description |
|---|---|
| purchase_intent | intention d’achat |
| product_question | question sur un produit |
| payment_question | question sur le paiement |
| shipping_question | question sur la livraison |
| other | commentaire général |
| unknown | intention inconnue ou ambiguë |

## 7. Structure des dossiers IA

La structure ajoutée pour le Bloc 2 est la suivante :

```text
src/
└── ai/
    ├── __init__.py
    ├── data_preparation/
    │   ├── __init__.py
    │   └── prepare_nlp_dataset.py
    ├── training/
    │   ├── __init__.py
    │   ├── train_intent_classifier.py
    │   └── benchmark_intent_models.py
    ├── inference/
    │   ├── __init__.py
    │   └── intent_predictor.py
    └── monitoring/
        ├── __init__.py
        └── monitor_predictions.py
```

Données et rapports IA :

```text
data/
└── ai/
    ├── datasets/
    ├── reports/
    └── predictions/
```

Modèles IA :

```text
models/
└── intent_classifier/
```

## 8. Préparation du dataset NLP

Le script responsable de la préparation du dataset NLP est :

```text
src/ai/data_preparation/prepare_nlp_dataset.py
```

Il lit :

```text
data/processed/clean/live_comments_clean.csv
```

Il génère :

```text
data/ai/datasets/comments_intent_dataset.csv
data/ai/datasets/train.csv
data/ai/datasets/validation.csv
data/ai/datasets/test.csv
```

## 9. Règles de préparation des données

Les règles de préparation sont les suivantes :

- supprimer les lignes sans texte de commentaire ;
- supprimer les lignes sans label cible ;
- normaliser les espaces dans les commentaires ;
- conserver uniquement les classes autorisées ;
- conserver les colonnes utiles à l’entraînement ;
- vérifier la distribution des classes ;
- séparer les données en train, validation et test ;
- produire des rapports de qualité.

Colonnes conservées dans le dataset NLP :

```text
comment_id
live_id
customer_id
platform
comment_text
comment_language
manual_intent_label
```

## 10. Séparation train / validation / test

La séparation prévue est :

| Jeu | Pourcentage | Utilisation |
|---|---:|---|
| train | 70 % | entraînement du modèle |
| validation | 15 % | comparaison et réglage |
| test | 15 % | évaluation finale |

Les fichiers générés sont :

```text
data/ai/datasets/train.csv
data/ai/datasets/validation.csv
data/ai/datasets/test.csv
```

La séparation doit être reproductible grâce à un `random_state`.

## 11. Rapports de préparation attendus

Le script de préparation du dataset doit générer :

```text
data/ai/reports/nlp_dataset_quality_report.csv
data/ai/reports/train_validation_test_split_report.csv
```

Le rapport qualité doit contenir :

- nombre total de commentaires ;
- nombre de commentaires conservés ;
- nombre de commentaires supprimés ;
- nombre de labels manquants ;
- nombre de commentaires vides ;
- distribution des classes ;
- statut global du dataset.

Le rapport de séparation doit contenir :

- nombre de lignes dans le train ;
- nombre de lignes dans la validation ;
- nombre de lignes dans le test ;
- distribution des classes par jeu ;
- pourcentage de chaque jeu.

## 12. Modèle principal retenu

Le modèle principal retenu pour la première version est :

```text
TF-IDF + Logistic Regression
```

Cette approche est composée de deux parties :

1. vectorisation du texte avec TF-IDF ;
2. classification avec une régression logistique.

Le modèle sera entraîné dans :

```text
src/ai/training/train_intent_classifier.py
```

## 13. Vectorisation du texte

Le texte sera converti en variables numériques avec une vectorisation TF-IDF.

Paramètres prévus :

```text
lowercase=True
ngram_range=(1, 2)
min_df=1
max_features=5000
```

Objectif :

- transformer les commentaires en représentation numérique ;
- conserver les mots et groupes de mots importants ;
- obtenir une matrice compatible avec un modèle de classification.

## 14. Modèle de classification

Le classifieur principal sera une régression logistique.

Paramètres prévus :

```text
max_iter=1000
class_weight="balanced"
random_state=42
```

Le paramètre `class_weight="balanced"` est utilisé pour limiter l’impact d’un déséquilibre entre les classes.

## 15. Artefacts du modèle

Après entraînement, les artefacts seront sauvegardés dans :

```text
models/intent_classifier/
```

Fichiers attendus :

```text
model.joblib
vectorizer.joblib
label_encoder.joblib
model_metadata.json
```

Description des fichiers :

| Fichier | Description |
|---|---|
| model.joblib | modèle entraîné |
| vectorizer.joblib | transformateur TF-IDF |
| label_encoder.joblib | encodeur des labels |
| model_metadata.json | informations techniques sur le modèle |

## 16. Métadonnées du modèle

Le fichier `model_metadata.json` doit contenir :

```json
{
  "model_name": "intent_classifier",
  "model_version": "intent_classifier_v1",
  "algorithm": "TF-IDF + Logistic Regression",
  "training_date": "YYYY-MM-DD HH:MM:SS",
  "classes": [
    "purchase_intent",
    "product_question",
    "payment_question",
    "shipping_question",
    "other",
    "unknown"
  ],
  "train_file": "data/ai/datasets/train.csv",
  "validation_file": "data/ai/datasets/validation.csv",
  "test_file": "data/ai/datasets/test.csv"
}
```

## 17. Évaluation du modèle

Le modèle sera évalué sur le jeu de test.

Métriques attendues :

| Métrique | Description |
|---|---|
| accuracy | taux global de bonnes prédictions |
| precision | qualité des prédictions positives |
| recall | capacité à retrouver les exemples d’une classe |
| f1-score | équilibre entre précision et rappel |
| confusion matrix | matrice des erreurs de classification |

Rapports générés :

```text
data/ai/reports/model_training_report.csv
data/ai/reports/model_evaluation_report.csv
data/ai/reports/classification_report.csv
data/ai/reports/confusion_matrix.csv
```

## 18. Benchmark des modèles

Le benchmark sera réalisé dans :

```text
src/ai/training/benchmark_intent_models.py
```

Approches comparées :

| Modèle | Rôle |
|---|---|
| DummyClassifier | baseline minimale |
| règles simples | baseline métier |
| TF-IDF + Logistic Regression | modèle principal |
| TF-IDF + Linear SVM | comparaison texte |
| TF-IDF + Random Forest | comparaison secondaire |

Sortie attendue :

```text
data/ai/reports/model_benchmark_report.csv
```

Le benchmark permettra de justifier le choix du modèle final.

## 19. Chargement du modèle pour inférence

Le chargement du modèle sera réalisé dans :

```text
src/ai/inference/intent_predictor.py
```

Ce module devra permettre :

- de charger le modèle sauvegardé ;
- de charger le vectorizer ;
- de charger le label encoder ;
- de prédire une intention pour un commentaire ;
- de retourner un score de confiance ;
- de retourner la version du modèle.

Fonctions prévues :

```text
load_model_artifacts()
predict_intent(comment_text)
predict_batch(comment_texts)
get_model_info()
```

## 20. Format de prédiction unitaire

Entrée :

```python
"je prends le pull rouge en M"
```

Sortie Python attendue :

```python
{
    "comment_text": "je prends le pull rouge en M",
    "predicted_intent": "purchase_intent",
    "confidence_score": 0.91,
    "model_version": "intent_classifier_v1"
}
```

## 21. Format de prédiction batch

Entrée :

```json
{
  "comments": [
    "je prends le pull rouge en M",
    "vous livrez en Belgique ?",
    "trop beau"
  ]
}
```

Sortie :

```json
{
  "predictions": [
    {
      "comment_text": "je prends le pull rouge en M",
      "predicted_intent": "purchase_intent",
      "confidence_score": 0.91,
      "model_version": "intent_classifier_v1"
    },
    {
      "comment_text": "vous livrez en Belgique ?",
      "predicted_intent": "shipping_question",
      "confidence_score": 0.87,
      "model_version": "intent_classifier_v1"
    },
    {
      "comment_text": "trop beau",
      "predicted_intent": "other",
      "confidence_score": 0.76,
      "model_version": "intent_classifier_v1"
    }
  ]
}
```

## 22. Intégration API

Le service IA sera intégré dans l’API FastAPI existante.

Fichiers prévus :

```text
api/ai_service.py
api/routes/ai.py
```

Le fichier `api/ai_service.py` servira d’interface entre FastAPI et le module d’inférence.

Le fichier `api/routes/ai.py` contiendra les routes REST IA.

## 23. Routes API IA prévues

| Méthode | Route | Description |
|---|---|---|
| POST | /api/v1/ai/predict-intent | prédire l’intention d’un commentaire |
| POST | /api/v1/ai/batch-predict-intents | prédire plusieurs commentaires |
| GET | /api/v1/ai/model-info | retourner les informations du modèle |
| GET | /api/v1/ai/model-metrics | retourner les métriques du modèle |

## 24. Sécurité des routes IA

Les routes IA seront protégées avec la même méthode que les routes du Bloc 1 :

```text
X-API-Key
```

Un appel sans clé API doit retourner :

```text
401 Unauthorized
```

Un appel avec une mauvaise clé API doit retourner :

```text
403 Forbidden
```

Un appel avec une clé API valide doit retourner :

```text
200 OK
```

## 25. Documentation API

Les routes IA seront visibles dans la documentation Swagger de FastAPI.

URL locale :

```text
http://127.0.0.1:8000/docs
```

Le schéma OpenAPI sera disponible ici :

```text
http://127.0.0.1:8000/openapi.json
```

Chaque route devra avoir :

- un nom clair ;
- une description ;
- un modèle d’entrée ;
- un modèle de sortie ;
- des codes d’erreur documentés.

## 26. Schémas API attendus

Les schémas Pydantic attendus sont :

```text
IntentPredictionRequest
IntentPredictionResponse
BatchIntentPredictionRequest
BatchIntentPredictionResponse
ModelInfoResponse
ModelMetricsResponse
```

Ces schémas permettront de valider les entrées et sorties de l’API.

## 27. Exemple de requête API

Requête PowerShell :

```powershell
$headers = @{ "X-API-Key" = "paylive-dev-api-key" }

$body = @{
    comment_text = "je prends le pull rouge en M"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/ai/predict-intent" `
  -Method POST `
  -Headers $headers `
  -Body $body `
  -ContentType "application/json"
```

Réponse attendue :

```json
{
  "comment_text": "je prends le pull rouge en M",
  "predicted_intent": "purchase_intent",
  "confidence_score": 0.91,
  "model_version": "intent_classifier_v1"
}
```

## 28. Gestion des erreurs API

Les erreurs attendues sont :

| Code | Cas |
|---|---|
| 400 | commentaire vide ou invalide |
| 401 | clé API absente |
| 403 | clé API invalide |
| 404 | modèle ou métriques non disponibles |
| 500 | erreur interne lors de la prédiction |

Exemple de réponse en cas de commentaire vide :

```json
{
  "detail": "Comment text cannot be empty."
}
```

## 29. Tests automatisés

Les tests automatisés seront organisés dans :

```text
tests/test_ai_dataset.py
tests/test_intent_model.py
tests/test_ai_api.py
```

## 30. Tests du dataset IA

Le fichier `tests/test_ai_dataset.py` devra vérifier :

- que le dataset NLP existe ;
- que les fichiers train, validation et test existent ;
- que les commentaires ne sont pas vides ;
- que les labels sont présents ;
- que les classes attendues existent ;
- que les rapports de préparation sont générés.

## 31. Tests du modèle IA

Le fichier `tests/test_intent_model.py` devra vérifier :

- que les artefacts du modèle existent ;
- que le modèle peut être chargé ;
- que le vectorizer peut être chargé ;
- que le label encoder peut être chargé ;
- qu’une prédiction simple fonctionne ;
- que le score de confiance est compris entre 0 et 1 ;
- que la classe prédite appartient aux classes attendues.

## 32. Tests de l’API IA

Le fichier `tests/test_ai_api.py` devra vérifier :

- que les routes IA sont protégées ;
- qu’un appel sans clé API retourne 401 ;
- qu’un appel avec mauvaise clé retourne 403 ;
- qu’un appel valide retourne 200 ;
- que la route de prédiction retourne le bon format ;
- que la route batch retourne une liste de prédictions ;
- que la route model-info fonctionne ;
- que la route model-metrics fonctionne.

## 33. Rapports de tests

Les tests IA pourront générer des rapports dans :

```text
data/ai/reports/
```

Fichiers possibles :

```text
ai_dataset_test_report.csv
intent_model_test_report.csv
ai_api_test_report.csv
```

## 34. Monitoring des prédictions

Le monitoring sera réalisé dans :

```text
src/ai/monitoring/monitor_predictions.py
```

Les prédictions seront historisées dans :

```text
data/ai/predictions/ai_predictions_log.csv
```

Chaque prédiction devra enregistrer :

| Champ | Description |
|---|---|
| prediction_id | identifiant unique |
| predicted_at | date de prédiction |
| comment_text | commentaire analysé |
| predicted_intent | classe prédite |
| confidence_score | score de confiance |
| model_version | version du modèle |
| response_time_ms | temps de réponse |
| source | origine de la prédiction |

## 35. Rapport de monitoring

Le rapport de monitoring sera généré ici :

```text
data/ai/reports/model_monitoring_report.csv
```

Il devra contenir :

- nombre total de prédictions ;
- nombre de prédictions par classe ;
- score moyen de confiance ;
- score minimum ;
- score maximum ;
- nombre de prédictions à faible confiance ;
- temps moyen de prédiction ;
- modèle utilisé.

## 36. Seuil de faible confiance

Un seuil de faible confiance sera défini.

Valeur prévue :

```text
0.60
```

Si le score de confiance est inférieur à ce seuil, la prédiction sera considérée comme incertaine.

Ces prédictions pourront être utilisées plus tard pour :

- correction manuelle ;
- amélioration du dataset ;
- réentraînement du modèle.

## 37. Contraintes RGPD et données personnelles

Le projet utilise des données simulées.

Cependant, dans un cas réel, les commentaires de live peuvent contenir :

- noms ;
- pseudonymes ;
- informations personnelles ;
- adresses ;
- demandes liées à une commande.

Mesures retenues dans le projet :

- aucune donnée réelle PayLive ;
- données clients simulées ;
- identifiants pseudonymisés ;
- absence de données bancaires ;
- pas d’exposition des emails via l’API IA ;
- journalisation limitée aux besoins techniques ;
- documentation dans le registre RGPD du projet.

## 38. Sécurité technique

Mesures de sécurité prévues :

- routes protégées par clé API ;
- clé API stockée dans `.env` ;
- `.env` exclu de Git ;
- validation des entrées avec Pydantic ;
- pas d’exécution de code utilisateur ;
- pas de dépendance obligatoire à un service IA externe ;
- logs contrôlés ;
- limitation des informations retournées en cas d’erreur.

## 39. Limites techniques

La première version du service IA présente certaines limites :

- le modèle dépend de la qualité des labels simulés ;
- les commentaires très courts peuvent être difficiles à classifier ;
- les fautes d’orthographe peuvent réduire la performance ;
- le modèle TF-IDF ne comprend pas réellement le contexte ;
- le modèle ne fait pas encore d’extraction fine produit / taille / couleur / quantité ;
- le modèle n’est pas encore déployé en production cloud.

## 40. Évolutions techniques possibles

Évolutions possibles :

- ajout d’un modèle transformer local ;
- ajout d’un modèle multilingue ;
- ajout de l’extraction produit ;
- ajout de l’extraction taille ;
- ajout de l’extraction couleur ;
- ajout de l’extraction quantité ;
- ajout d’un retour utilisateur ;
- ajout d’un système de réentraînement ;
- ajout d’un suivi de drift ;
- ajout d’un tableau de bord de monitoring.

## 41. Dépendances Python prévues

Les dépendances principales du Bloc 2 sont :

```text
scikit-learn
joblib
pandas
numpy
fastapi
uvicorn
pydantic
pytest
httpx
python-dotenv
```

Les dépendances avancées suivantes ne sont pas nécessaires pour la première version :

```text
transformers
torch
sentence-transformers
```

Elles pourront être ajoutées plus tard si un modèle NLP avancé est intégré.

## 42. Commandes prévues

Préparation du dataset :

```bash
python src/ai/data_preparation/prepare_nlp_dataset.py
```

Entraînement du modèle :

```bash
python src/ai/training/train_intent_classifier.py
```

Benchmark :

```bash
python src/ai/training/benchmark_intent_models.py
```

Monitoring :

```bash
python src/ai/monitoring/monitor_predictions.py
```

Tests IA :

```bash
pytest tests/test_ai_dataset.py -v
pytest tests/test_intent_model.py -v
pytest tests/test_ai_api.py -v
```

API :

```bash
python -m uvicorn api.main:app --reload
```

## 43. Critères de validation technique

Le service IA sera considéré comme valide si :

- le dataset NLP est généré ;
- les jeux train, validation et test sont générés ;
- le modèle est entraîné sans erreur ;
- les artefacts modèle sont sauvegardés ;
- les métriques d’évaluation sont produites ;
- le benchmark est disponible ;
- l’API charge correctement le modèle ;
- une prédiction unitaire fonctionne ;
- une prédiction batch fonctionne ;
- les routes IA sont protégées ;
- les tests automatisés passent ;
- le monitoring génère un rapport.

## 44. Conclusion

Ces spécifications techniques définissent la première version du service IA du projet **PayLive AI Copilot**.

Le service IA repose sur une approche locale, simple, explicable et testable.

Il permet de transformer les commentaires nettoyés du Bloc 1 en prédictions d’intention exploitables par API REST.

Cette première version constitue une base solide pour intégrer ensuite des fonctionnalités plus avancées, comme l’extraction automatique du produit, de la taille, de la couleur ou de la quantité.