# Bilan du Bloc 2 — PayLive AI Copilot

## 1. Objectif du document

Ce document présente le bilan du Bloc 2 du projet **PayLive AI Copilot**.

Le Bloc 2 avait pour objectif d’intégrer un service d’intelligence artificielle permettant d’analyser les commentaires de live shopping et de prédire l’intention exprimée par l’utilisateur.

## 2. Rappel du besoin

Pendant un live shopping, les vendeurs reçoivent de nombreux commentaires.

Certains commentaires expriment une intention d’achat, tandis que d’autres correspondent à des questions produit, paiement, livraison ou à des réactions générales.

Le besoin IA est donc de classifier automatiquement les commentaires pour aider le vendeur à identifier les messages les plus importants.

## 3. Fonctionnalité IA réalisée

La fonctionnalité principale développée est :

```text
classification d’intention des commentaires de live shopping
```

Exemple :

```text
"je prends la robe noire en M" → purchase_intent
```

Classes prédites :

```text
purchase_intent
product_question
payment_question
shipping_question
other
unknown
```

## 4. Travaux réalisés

Le Bloc 2 a couvert les travaux suivants :

1. cadrage du besoin IA ;
2. rédaction des spécifications du service IA ;
3. veille technique et réglementaire ;
4. benchmark théorique des solutions IA ;
5. préparation du dataset NLP ;
6. entraînement d’un modèle baseline ;
7. évaluation du modèle ;
8. benchmark interne de plusieurs modèles ;
9. sélection du modèle final ;
10. développement du module d’inférence ;
11. intégration dans l’API REST ;
12. sécurisation des routes IA ;
13. tests automatisés ;
14. monitoring des prédictions ;
15. documentation technique.

## 5. Documentation produite

```text
docs/07_ai_service/21_cadrage_bloc2_ia.md
docs/07_ai_service/22_specifications_service_ia.md
docs/07_ai_service/23_veille_technique_reglementaire_ia.md
docs/07_ai_service/24_benchmark_modeles_services_ia.md
docs/07_ai_service/25_preparation_dataset_nlp.md
docs/07_ai_service/26_entrainement_evaluation_modele.md
docs/07_ai_service/27_api_service_ia.md
docs/07_ai_service/28_tests_service_ia.md
docs/07_ai_service/29_monitoring_modele_ia.md
docs/07_ai_service/30_bilan_bloc2.md
```

## 6. Scripts développés

```text
src/ai/data_preparation/prepare_nlp_dataset.py
src/ai/training/train_intent_classifier.py
src/ai/training/benchmark_intent_models.py
src/ai/inference/intent_predictor.py
src/ai/monitoring/monitor_predictions.py
```

## 7. API IA développée

Fichiers API ajoutés ou modifiés :

```text
api/ai_service.py
api/routes/ai.py
api/main.py
```

Routes IA disponibles :

```text
POST /api/v1/ai/predict-intent
POST /api/v1/ai/batch-predict-intents
GET  /api/v1/ai/model-info
GET  /api/v1/ai/model-metrics
```

Les routes sont protégées par :

```text
X-API-Key
```

## 8. Tests développés

```text
tests/test_ai_dataset.py
tests/test_intent_model.py
tests/test_ai_api.py
```

Ces tests couvrent les datasets IA, les artefacts du modèle, les prédictions, les routes API, la sécurité par clé API, OpenAPI et les rapports de tests.

## 9. Fichiers générés

Datasets IA :

```text
data/ai/datasets/comments_intent_dataset.csv
data/ai/datasets/train.csv
data/ai/datasets/validation.csv
data/ai/datasets/test.csv
```

Rapports IA :

```text
data/ai/reports/nlp_dataset_quality_report.csv
data/ai/reports/train_validation_test_split_report.csv
data/ai/reports/model_training_report.csv
data/ai/reports/model_evaluation_report.csv
data/ai/reports/classification_report.csv
data/ai/reports/confusion_matrix.csv
data/ai/reports/model_benchmark_report.csv
data/ai/reports/model_benchmark_classification_report.csv
data/ai/reports/model_benchmark_selection_report.csv
data/ai/reports/ai_dataset_test_report.csv
data/ai/reports/intent_model_test_report.csv
data/ai/reports/ai_api_test_report.csv
data/ai/reports/model_monitoring_report.csv
```

Artefacts modèle :

```text
models/intent_classifier/model.joblib
models/intent_classifier/vectorizer.joblib
models/intent_classifier/label_encoder.joblib
models/intent_classifier/model_metadata.json
```

Monitoring :

```text
data/ai/predictions/ai_predictions_log.csv
```

## 10. Modèle retenu

Le modèle retenu est :

```text
TF-IDF + Logistic Regression
```

Le benchmark interne a sélectionné :

```text
tfidf_logistic_regression
```

Résultats observés :

```text
Test accuracy: 0.8
Test macro F1: 0.6
Test weighted F1: 0.72
```

Sélection benchmark :

```text
validation_accuracy = 0.8
validation_macro_f1 = 0.6667
validation_weighted_f1 = 0.7333
```

## 11. Justification du modèle choisi

Le modèle a été choisi car il offre un bon compromis entre performance, simplicité, explicabilité, rapidité, fonctionnement local, intégration API, disponibilité d’un score de confiance et facilité de test.

## 12. Tests finaux Bloc 2

Commandes de validation :

```bash
python src/ai/data_preparation/prepare_nlp_dataset.py
python src/ai/training/train_intent_classifier.py
python src/ai/training/benchmark_intent_models.py
python src/ai/monitoring/monitor_predictions.py
pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py -v
```

Résultat attendu :

```text
tous les tests passed
```

## 13. Lancement API

Avec Uvicorn :

```bash
python -m uvicorn api.main:app --reload
```

Avec Docker Compose :

```bash
docker compose up -d --build
```

Documentation Swagger :

```text
http://127.0.0.1:8000/docs
```

Health check :

```text
http://127.0.0.1:8000/health
```

## 14. Points forts du Bloc 2

- chaîne IA complète de bout en bout ;
- dataset NLP préparé automatiquement ;
- modèle entraîné et sauvegardé ;
- benchmark de plusieurs modèles ;
- API IA sécurisée ;
- documentation OpenAPI ;
- tests automatisés ;
- monitoring des prédictions ;
- fonctionnement local et reproductible ;
- cohérence avec les données du Bloc 1.

## 15. Difficultés rencontrées

1. labels incohérents dans le dataset NLP ;
2. classes absentes dans les premiers splits ;
3. métriques initiales à zéro ;
4. confiance faible sur certaines prédictions ;
5. erreur d’import lors de l’intégration du monitoring dans Docker.

## 16. Corrections apportées

- consolidation des labels à partir du texte ;
- ajout d’exemples synthétiques contrôlés ;
- suppression des doublons textuels ;
- benchmark pour valider le modèle ;
- ajout d’un seuil de faible confiance ;
- redémarrage ou reconstruction Docker après modification du monitoring.

## 17. Limites actuelles

- données simulées ;
- dataset limité ;
- modèle simple ;
- pas d’extraction fine produit / taille / couleur / quantité ;
- monitoring local en CSV ;
- pas de dashboard MLOps ;
- pas de réentraînement automatique.

## 18. Évolutions possibles

- modèle transformer local ;
- modèle multilingue ;
- extraction du produit ;
- extraction de la taille ;
- extraction de la couleur ;
- extraction de la quantité ;
- stockage du monitoring en base PostgreSQL ;
- tableau de bord de monitoring ;
- boucle de correction humaine ;
- réentraînement automatique.

## 19. Correspondance avec les attentes du Bloc 2

| Attente | Réalisation |
|---|---|
| veille technique et réglementaire | document 23 |
| benchmark de solutions IA | documents 24 et 26 |
| préparation des données IA | script prepare_nlp_dataset.py |
| entraînement du modèle | script train_intent_classifier.py |
| évaluation du modèle | rapports d’évaluation |
| comparaison de modèles | benchmark_intent_models.py |
| exposition via API REST | routes IA FastAPI |
| sécurisation API | X-API-Key |
| documentation API | Swagger / OpenAPI |
| tests automatisés | tests IA et API |
| monitoring | log de prédictions et rapport monitoring |

## 20. Emplacements pour captures d’écran

```text
[CAPTURE À AJOUTER]
Pipeline Bloc 2 exécuté sans erreur
```

```text
[CAPTURE À AJOUTER]
Swagger avec routes IA
```

```text
[CAPTURE À AJOUTER]
Résultat pytest des tests IA
```

```text
[CAPTURE À AJOUTER]
Fichiers générés dans data/ai/reports
```

```text
[CAPTURE À AJOUTER]
Fichiers générés dans models/intent_classifier
```

## 21. Conclusion

Le Bloc 2 est fonctionnellement terminé.

Le projet dispose maintenant d’un service IA capable de préparer un dataset NLP, entraîner un modèle de classification, comparer plusieurs modèles, sélectionner un modèle final, prédire une intention de commentaire, exposer le modèle par API REST, sécuriser les routes, tester automatiquement le service et monitorer les prédictions.

Cette étape transforme le socle de données du Bloc 1 en un service IA exploitable.

Le projet peut maintenant passer au Bloc 3, qui portera sur l’intégration applicative, l’industrialisation, l’interface utilisateur, les tests avancés, la CI/CD et le suivi opérationnel.
