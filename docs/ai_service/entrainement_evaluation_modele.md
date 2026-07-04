# Entraînement, évaluation et benchmark du modèle IA — PayLive AI Copilot

## 1. Objectif du document

Ce document présente l’entraînement, l’évaluation et le benchmark des modèles de classification d’intentions du projet **PayLive AI Copilot**.

L’objectif est de sélectionner un modèle IA capable de prédire l’intention d’un commentaire de live shopping.

## 2. Problème traité

Le problème traité est une classification supervisée de texte.

Entrée :

```text
comment_text
```

Sortie :

```text
manual_intent_label
```

Exemple :

```text
"je prends la robe noire en M" → purchase_intent
```

## 3. Données utilisées

Les fichiers utilisés pour l’entraînement sont :

```text
data/ai/datasets/train.csv
data/ai/datasets/validation.csv
data/ai/datasets/test.csv
```

Ces fichiers sont générés par :

```text
src/ai/data_preparation/prepare_nlp_dataset.py
```

## 4. Modèle baseline retenu

Le premier modèle entraîné est :

```text
TF-IDF + Logistic Regression
```

Cette approche a été retenue comme baseline principale car elle est simple, rapide, adaptée aux textes courts, compatible avec un dataset limité, facilement intégrable dans une API et capable de produire un score de confiance.

## 5. Script d’entraînement

Le script utilisé est :

```text
src/ai/training/train_intent_classifier.py
```

Il réalise les étapes suivantes :

1. chargement des datasets train, validation et test ;
2. validation des colonnes obligatoires ;
3. encodage des labels ;
4. vectorisation TF-IDF des commentaires ;
5. entraînement d’une régression logistique ;
6. prédiction sur validation et test ;
7. calcul des métriques ;
8. génération des rapports ;
9. sauvegarde du modèle et des artefacts.

## 6. Vectorisation TF-IDF

Le texte est transformé en variables numériques grâce à TF-IDF.

Paramètres principaux :

```text
lowercase=True
ngram_range=(1, 2)
min_df=1
max_features=5000
```

Cette vectorisation permet de représenter les commentaires en tenant compte des mots et groupes de mots significatifs.

## 7. Classifieur

Le classifieur utilisé est une régression logistique.

Paramètres principaux :

```text
max_iter=1000
class_weight="balanced"
random_state=42
```

Le paramètre `class_weight="balanced"` limite l’impact d’un éventuel déséquilibre entre classes.

## 8. Artefacts générés

Les artefacts du modèle sont sauvegardés dans :

```text
models/intent_classifier/
```

Fichiers générés :

```text
model.joblib
vectorizer.joblib
label_encoder.joblib
model_metadata.json
```

| Fichier | Description |
|---|---|
| model.joblib | modèle Logistic Regression entraîné |
| vectorizer.joblib | vectorizer TF-IDF |
| label_encoder.joblib | encodeur des labels |
| model_metadata.json | métadonnées du modèle |

## 9. Rapports d’évaluation générés

Les rapports sont sauvegardés dans :

```text
data/ai/reports/
```

Fichiers générés :

```text
model_training_report.csv
model_evaluation_report.csv
classification_report.csv
confusion_matrix.csv
```

## 10. Métriques utilisées

| Métrique | Rôle |
|---|---|
| accuracy | taux global de bonnes prédictions |
| precision | proportion de prédictions correctes pour une classe |
| recall | capacité à retrouver les exemples d’une classe |
| f1-score | équilibre entre precision et recall |
| macro F1 | moyenne simple entre classes |
| weighted F1 | moyenne pondérée par le nombre d’exemples |
| confusion matrix | visualisation des erreurs de classification |

## 11. Résultat de la baseline

Après correction du dataset, le modèle baseline a obtenu :

```text
Test accuracy: 0.8
Test macro F1: 0.6
Test weighted F1: 0.72
```

Interprétation :

| Métrique | Interprétation |
|---|---|
| accuracy = 0.8 | 80 % des commentaires du test sont correctement prédits |
| macro F1 = 0.6 | certaines classes restent plus difficiles |
| weighted F1 = 0.72 | performance globale correcte pour une première version |

Ces résultats sont acceptables pour une baseline pédagogique.

## 12. Problème rencontré pendant l’entraînement

Lors du premier entraînement, les métriques étaient nulles :

```text
Test accuracy: 0.0
Test macro F1: 0.0
Test weighted F1: 0.0
```

Analyse du problème :

- certaines classes étaient absentes ;
- plusieurs commentaires identiques avaient des labels différents ;
- le modèle ne pouvait donc pas apprendre correctement.

Correction apportée :

- consolidation des labels à partir du texte ;
- ajout d’exemples synthétiques contrôlés ;
- suppression des doublons textuels ;
- régénération du dataset NLP.

Après correction, les métriques sont devenues cohérentes.

## 13. Benchmark interne

Un benchmark interne a été réalisé pour comparer plusieurs approches.

Script utilisé :

```text
src/ai/training/benchmark_intent_models.py
```

Modèles comparés :

| Modèle | Rôle |
|---|---|
| business_rules_baseline | baseline métier par règles |
| dummy_most_frequent | baseline naïve |
| tfidf_logistic_regression | modèle principal |
| tfidf_linear_svm | comparaison ML texte |
| tfidf_multinomial_nb | comparaison probabiliste |
| tfidf_random_forest | comparaison non linéaire |

## 14. Rapports de benchmark

Le benchmark génère :

```text
data/ai/reports/model_benchmark_report.csv
data/ai/reports/model_benchmark_classification_report.csv
data/ai/reports/model_benchmark_selection_report.csv
```

Le rapport de sélection indique le modèle retenu selon :

```text
validation weighted_f1, puis macro_f1, puis accuracy
```

## 15. Modèle sélectionné

Le benchmark a sélectionné :

```text
tfidf_logistic_regression
```

Métriques de validation observées :

```text
validation_accuracy = 0.8
validation_macro_f1 = 0.6667
validation_weighted_f1 = 0.7333
```

Ce résultat confirme le choix initial du modèle principal.

## 16. Justification du choix final

Le modèle final retenu est :

```text
TF-IDF + Logistic Regression
```

Justification :

- meilleures métriques de validation parmi les modèles éligibles ;
- temps d’entraînement faible ;
- intégration simple dans FastAPI ;
- score de confiance disponible ;
- modèle local ;
- pas de dépendance à un service externe ;
- fonctionnement reproductible ;
- simplicité d’explication.

## 17. Commandes d’exécution

```bash
python src/ai/data_preparation/prepare_nlp_dataset.py
python src/ai/training/train_intent_classifier.py
python src/ai/training/benchmark_intent_models.py
```

## 18. Contrôles manuels

Vérifier les artefacts :

```bash
dir models\intent_classifier
```

Vérifier les rapports :

```bash
dir data\ai\reports
```

Vérifier le modèle sélectionné :

```bash
python -c "import pandas as pd; print(pd.read_csv('data/ai/reports/model_benchmark_selection_report.csv').to_string(index=False))"
```

## 19. Emplacements pour captures d’écran

```text
[CAPTURE À AJOUTER]
Terminal montrant l’entraînement réussi de train_intent_classifier.py
```

```text
[CAPTURE À AJOUTER]
Dossier models/intent_classifier avec les artefacts sauvegardés
```

```text
[CAPTURE À AJOUTER]
Sortie du benchmark montrant le modèle sélectionné
```

```text
[CAPTURE À AJOUTER]
Extrait de model_evaluation_report.csv ou model_benchmark_report.csv
```

## 20. Limites du modèle

Limites identifiées :

- dataset encore limité ;
- labels simulés ;
- certains commentaires ambigus ;
- score de confiance parfois faible ;
- modèle sensible aux formulations inconnues ;
- compréhension contextuelle limitée.

## 21. Conclusion

L’entraînement et le benchmark ont permis de valider un premier modèle IA fonctionnel.

Le modèle **TF-IDF + Logistic Regression** est retenu pour l’intégration API car il présente le meilleur compromis entre performance, simplicité, explicabilité et intégration technique.
