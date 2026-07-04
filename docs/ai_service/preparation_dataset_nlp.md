# Préparation du dataset NLP — PayLive AI Copilot

## 1. Objectif du document

Ce document décrit la préparation du dataset NLP utilisé dans le Bloc 2 du projet **PayLive AI Copilot**.

L’objectif est de transformer les commentaires nettoyés issus du Bloc 1 en un dataset exploitable pour entraîner un modèle de classification d’intentions.

Le dataset NLP sert à apprendre au modèle à associer un commentaire de live shopping à une intention métier.

## 2. Rappel du besoin IA

Le service IA doit analyser automatiquement des commentaires de live shopping afin de prédire l’intention exprimée par l’utilisateur.

Exemples :

| Commentaire | Label attendu |
|---|---|
| je prends le pull rouge en M | purchase_intent |
| comment payer ? | payment_question |
| vous livrez en Belgique ? | shipping_question |
| elle existe en noir ? | product_question |
| trop beau | other |
| je ne sais pas | unknown |

## 3. Source de données utilisée

La préparation du dataset NLP s’appuie sur les données nettoyées du Bloc 1.

Fichier source :

```text
data/processed/clean/live_comments_clean.csv
```

Ce fichier est produit par le pipeline de nettoyage et normalisation des données.

## 4. Colonnes utilisées

| Colonne | Rôle |
|---|---|
| comment_id | identifiant du commentaire |
| live_id | identifiant du live associé |
| customer_id | identifiant pseudonymisé de l’utilisateur |
| platform | plateforme du commentaire |
| comment_text | texte à analyser |
| comment_language | langue du commentaire |
| manual_intent_label | label cible |
| data_quality_status | statut qualité de la donnée |

La colonne d’entrée du modèle est `comment_text`.

La colonne cible est `manual_intent_label`.

## 5. Script de préparation

Le script de préparation est :

```text
src/ai/data_preparation/prepare_nlp_dataset.py
```

Il réalise les étapes suivantes :

1. chargement des commentaires nettoyés ;
2. contrôle de la présence des colonnes obligatoires ;
3. normalisation légère du texte ;
4. normalisation des labels ;
5. consolidation des labels à partir du texte ;
6. suppression des commentaires vides ;
7. suppression des labels invalides ;
8. ajout d’exemples synthétiques pédagogiques pour équilibrer les classes ;
9. suppression des doublons textuels ;
10. création du dataset NLP final ;
11. séparation train / validation / test ;
12. génération des rapports de qualité.

## 6. Normalisation du texte

La normalisation du texte reste volontairement simple : suppression des espaces inutiles et conservation du sens original du commentaire.

Exemple :

```text
"   je prends   la robe noire   "  →  "je prends la robe noire"
```

## 7. Normalisation des labels

Les labels sont normalisés pour garantir une liste cohérente de classes.

| Label source possible | Label normalisé |
|---|---|
| purchase | purchase_intent |
| achat | purchase_intent |
| question_paiement | payment_question |
| livraison | shipping_question |
| question_produit | product_question |
| autre | other |
| inconnu | unknown |

Labels autorisés :

```text
purchase_intent
product_question
payment_question
shipping_question
other
unknown
```

## 8. Consolidation des labels

Lors des premiers tests, certains commentaires identiques avaient plusieurs labels différents.

Exemple de problème :

```text
Comment payer ?  → other
Comment payer ?  → payment_question
Comment payer ?  → purchase_intent
```

Ce type d’incohérence empêche le modèle d’apprendre correctement.

Pour corriger cela, une consolidation des labels a été ajoutée à partir du contenu du commentaire.

| Type de mots-clés | Label consolidé |
|---|---|
| payer, paiement, carte, PayPal, CB | payment_question |
| livraison, frais de port, relais, recevoir | shipping_question |
| je prends, je commande, réserve, panier | purchase_intent |
| prix, taille, couleur, stock, disponible | product_question |
| merci, coucou, super, trop beau | other |
| commentaire ambigu | unknown |

## 9. Ajout d’exemples synthétiques

Certaines classes étaient absentes ou sous-représentées dans le dataset généré.

Exemple observé :

```text
product_question  = 0
shipping_question = 0
```

Pour rendre toutes les classes apprenables, le script ajoute des exemples synthétiques contrôlés.

Cette décision est acceptable dans ce projet car les données sont simulées, le projet est une preuve de concept pédagogique et les exemples sont documentés.

## 10. Suppression des doublons

Après consolidation, le script conserve un seul label par commentaire unique. La suppression des doublons se fait sur `comment_text`.

Cela évite qu’un même texte apparaisse plusieurs fois avec des labels contradictoires.

## 11. Dataset NLP final

Fichier généré :

```text
data/ai/datasets/comments_intent_dataset.csv
```

Colonnes conservées :

```text
comment_id
live_id
customer_id
platform
comment_text
comment_language
manual_intent_label
```

## 12. Séparation train / validation / test

Le dataset est séparé en trois jeux :

| Jeu | Pourcentage | Utilisation |
|---|---:|---|
| train | 70 % | entraînement du modèle |
| validation | 15 % | comparaison et sélection |
| test | 15 % | évaluation finale |

Fichiers générés :

```text
data/ai/datasets/train.csv
data/ai/datasets/validation.csv
data/ai/datasets/test.csv
```

La séparation utilise un `random_state` pour garantir la reproductibilité.

## 13. Rapports générés

Le script génère deux rapports :

```text
data/ai/reports/nlp_dataset_quality_report.csv
data/ai/reports/train_validation_test_split_report.csv
```

Le rapport qualité contient le nombre de lignes initiales, le nombre de lignes finales, les commentaires supprimés, les labels invalides, les doublons supprimés, les exemples ajoutés et la distribution des classes.

Le rapport de séparation contient le nombre de lignes par jeu, le pourcentage de chaque jeu et la distribution des classes dans train, validation et test.

## 14. Commande d’exécution

```bash
python src/ai/data_preparation/prepare_nlp_dataset.py
```

## 15. Contrôle manuel

```bash
dir data\ai\datasets
dir data\ai\reports
```

Fichiers attendus :

```text
comments_intent_dataset.csv
train.csv
validation.csv
test.csv
nlp_dataset_quality_report.csv
train_validation_test_split_report.csv
```

## 16. Emplacements pour captures d’écran

```text
[CAPTURE À AJOUTER]
Terminal montrant l’exécution réussie de prepare_nlp_dataset.py
```

```text
[CAPTURE À AJOUTER]
Explorateur montrant les fichiers générés dans data/ai/datasets
```

```text
[CAPTURE À AJOUTER]
Extrait du rapport train_validation_test_split_report.csv
```

## 17. Résultat obtenu

La préparation du dataset a permis de produire un jeu de données NLP cohérent, structuré et exploitable pour l’entraînement.

Les incohérences de labels observées au début ont été corrigées par une consolidation basée sur le texte.

Les classes attendues sont maintenant présentes dans le dataset, ce qui permet d’entraîner un modèle de classification supervisée.

## 18. Conclusion

Cette étape transforme les commentaires nettoyés du Bloc 1 en un dataset IA exploitable.

Elle constitue la base de l’entraînement, de l’évaluation et du benchmark des modèles du Bloc 2.
