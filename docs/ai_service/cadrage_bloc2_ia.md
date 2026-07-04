# Cadrage du Bloc 2 IA — PayLive AI Copilot

## 1. Objectif du document

Ce document présente le cadrage du Bloc 2 du projet **PayLive AI Copilot**.

Après le Bloc 1, le projet dispose déjà d’un socle complet de données :

- un pipeline de collecte multi-sources ;
- des données brutes simulées ;
- des données nettoyées et normalisées ;
- un dataset final analytique ;
- une base PostgreSQL structurée ;
- une API REST permettant de mettre les données à disposition ;
- des rapports qualité, d’import, d’API et de conformité RGPD.

Le Bloc 2 a pour objectif d’ajouter une dimension d’intelligence artificielle au projet.

L’objectif principal est de développer un service IA capable d’analyser automatiquement les commentaires envoyés pendant un live shopping et de prédire l’intention exprimée par l’utilisateur.

Ce service IA doit permettre d’aider un vendeur à repérer plus rapidement les commentaires importants pendant un live, notamment ceux qui expriment une intention d’achat.

## 2. Rappel du contexte projet

**PayLive AI Copilot** est un assistant intelligent destiné aux vendeurs qui réalisent des ventes en direct sur des plateformes comme TikTok Live ou Instagram Live.

Pendant un live, les spectateurs envoient de nombreux commentaires. Ces commentaires peuvent avoir plusieurs objectifs :

- commander un produit ;
- poser une question sur un article ;
- demander des informations sur la livraison ;
- poser une question sur le paiement ;
- réagir simplement au live ;
- envoyer un message ambigu ou incomplet.

Dans un contexte réel, un live peut générer un grand volume de commentaires en peu de temps. Le vendeur ou son équipe peut alors avoir des difficultés à repérer rapidement les commentaires à forte valeur commerciale.

Le service IA du Bloc 2 doit répondre à ce besoin en automatisant l’analyse des commentaires.

## 3. Problématique IA

La problématique principale du Bloc 2 est la suivante :

```text
Comment détecter automatiquement l’intention exprimée dans un commentaire de live shopping afin d’aider un vendeur à prioriser les actions commerciales ?
```

Le modèle IA devra analyser un commentaire texte et prédire l’intention associée.

Exemples :

| Commentaire | Intention attendue |
|---|---|
| je prends le pull rouge en M | purchase_intent |
| je veux commander celui-là | purchase_intent |
| je prends 2 robes noires | purchase_intent |
| combien coûte cette robe ? | product_question |
| elle existe en noir ? | product_question |
| vous avez encore du stock ? | product_question |
| vous livrez en Belgique ? | shipping_question |
| les frais de livraison sont combien ? | shipping_question |
| livraison possible demain ? | shipping_question |
| je peux payer par carte ? | payment_question |
| le lien de paiement marche ? | payment_question |
| on peut payer avec PayPal ? | payment_question |
| trop beau | other |
| merci beaucoup | other |
| super live | other |
| je ne sais pas | unknown |

## 4. Objectif fonctionnel du service IA

Le service IA doit recevoir un commentaire texte et retourner une prédiction d’intention.

Entrée attendue :

```json
{
  "comment_text": "je prends le pull rouge en M"
}
```

Sortie attendue :

```json
{
  "comment_text": "je prends le pull rouge en M",
  "predicted_intent": "purchase_intent",
  "confidence_score": 0.91,
  "model_version": "intent_classifier_v1"
}
```

Le résultat doit être exploitable :

- par une API REST ;
- par une future interface vendeur ;
- par un système de priorisation des commentaires ;
- par un tableau de bord de suivi des intentions.

## 5. Objectifs techniques du Bloc 2

Le Bloc 2 doit permettre de mettre en place une chaîne IA complète.

Les objectifs techniques sont :

- préparer un dataset NLP à partir des commentaires nettoyés ;
- contrôler la qualité du dataset NLP ;
- séparer les données en jeux d’entraînement, validation et test ;
- entraîner un modèle de classification de texte ;
- évaluer le modèle avec des métriques adaptées ;
- comparer plusieurs approches IA dans un benchmark ;
- sauvegarder les artefacts du modèle entraîné ;
- exposer le modèle via une API REST ;
- sécuriser les routes IA avec une clé API ;
- tester automatiquement le dataset, le modèle et l’API IA ;
- produire des rapports de monitoring des prédictions.

## 6. Données utilisées

Les données utilisées pour le Bloc 2 proviennent du Bloc 1.

Le fichier principal utilisé est :

```text
data/processed/clean/live_comments_clean.csv
```

Ce fichier contient les commentaires nettoyés issus des lives simulés.

Colonnes principales utilisées :

| Colonne | Utilisation |
|---|---|
| comment_id | identifiant du commentaire |
| live_id | rattachement au live |
| customer_id | identifiant pseudonymisé du client |
| platform | plateforme du commentaire |
| username | nom utilisateur simulé ou pseudonymisé |
| comment_text | texte du commentaire |
| commented_at | date du commentaire |
| comment_language | langue du commentaire |
| manual_intent_label | label cible pour l’entraînement |
| extracted_product_keyword | mot-clé produit éventuellement détecté |
| data_quality_status | statut qualité de la donnée |

La colonne utilisée comme texte d’entrée du modèle est :

```text
comment_text
```

La colonne utilisée comme cible de prédiction est :

```text
manual_intent_label
```

## 7. Cible de prédiction

Le modèle doit prédire la classe d’intention du commentaire.

Classes prévues :

| Classe | Description |
|---|---|
| purchase_intent | le client exprime une intention d’achat |
| product_question | le client pose une question sur un produit |
| payment_question | le client pose une question sur le paiement |
| shipping_question | le client pose une question sur la livraison |
| other | commentaire général sans intention commerciale directe |
| unknown | intention inconnue, vide ou ambiguë |

La classe la plus importante pour le besoin métier est :

```text
purchase_intent
```

Cette classe permet d’identifier les commentaires pouvant déclencher une action commerciale.

## 8. Type de problème IA

Le problème traité est un problème de :

```text
classification supervisée de texte
```

Le modèle apprend à associer un texte à une catégorie d’intention à partir d’exemples déjà labellisés.

Dans ce projet, les labels sont simulés dans les données générées, puis nettoyés dans le pipeline du Bloc 1.

Le Bloc 2 ne cherche pas encore à générer du texte automatiquement. Il se concentre sur la prédiction d’une classe à partir d’un commentaire.

## 9. Approche IA retenue pour la première version

Pour la première version du service IA, l’approche retenue est :

```text
TF-IDF + Logistic Regression
```

Cette approche est adaptée au projet pour plusieurs raisons :

- elle est simple à comprendre ;
- elle est rapide à entraîner ;
- elle fonctionne bien sur des textes courts ;
- elle est compatible avec un dataset de taille limitée ;
- elle est facile à sauvegarder ;
- elle est facile à intégrer dans une API FastAPI ;
- elle permet de produire des métriques claires ;
- elle est adaptée à une preuve de concept pédagogique.

Cette approche servira de modèle principal pour la première version du Bloc 2.

## 10. Approches comparées dans le benchmark

Un benchmark sera réalisé afin de justifier le choix du modèle.

Les approches prévues sont :

| Approche | Rôle |
|---|---|
| règles simples | baseline explicative |
| DummyClassifier | baseline machine learning minimale |
| TF-IDF + Logistic Regression | modèle principal |
| TF-IDF + Linear SVM | comparaison ML texte |
| TF-IDF + Random Forest | comparaison secondaire |
| Transformer local | évolution possible |
| LLM externe | évolution possible non prioritaire |

La première version du projet restera locale et ne dépendra pas d’un service IA externe.

Ce choix permet de limiter :

- les coûts ;
- les dépendances externes ;
- les risques de confidentialité ;
- la complexité technique ;
- les difficultés de reproductibilité.

## 11. Métriques d’évaluation

Les métriques prévues sont :

| Métrique | Objectif |
|---|---|
| accuracy | mesurer le taux global de bonnes prédictions |
| precision | mesurer la fiabilité des prédictions par classe |
| recall | mesurer la capacité à retrouver les commentaires d’une classe |
| f1-score | équilibrer précision et rappel |
| confusion matrix | visualiser les confusions entre classes |

Une attention particulière sera portée à la classe :

```text
purchase_intent
```

Cette classe est la plus importante pour le besoin métier, car elle correspond aux commentaires qui peuvent déclencher une action commerciale.

## 12. Structure technique prévue

La structure IA ajoutée au projet sera la suivante :

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

Les données IA seront organisées dans :

```text
data/
└── ai/
    ├── datasets/
    ├── reports/
    └── predictions/
```

Les modèles seront sauvegardés dans :

```text
models/
└── intent_classifier/
```

## 13. Fichiers attendus

À la fin du Bloc 2, les principaux fichiers attendus sont :

```text
data/ai/datasets/comments_intent_dataset.csv
data/ai/datasets/train.csv
data/ai/datasets/validation.csv
data/ai/datasets/test.csv

data/ai/reports/nlp_dataset_quality_report.csv
data/ai/reports/train_validation_test_split_report.csv
data/ai/reports/model_training_report.csv
data/ai/reports/model_evaluation_report.csv
data/ai/reports/model_benchmark_report.csv
data/ai/reports/model_monitoring_report.csv

data/ai/predictions/ai_predictions_log.csv

models/intent_classifier/model.joblib
models/intent_classifier/vectorizer.joblib
models/intent_classifier/label_encoder.joblib
models/intent_classifier/model_metadata.json
```

## 14. API IA prévue

Le modèle sera exposé via l’API FastAPI existante.

Routes prévues :

| Méthode | Route | Description |
|---|---|---|
| POST | /api/v1/ai/predict-intent | prédire l’intention d’un commentaire |
| POST | /api/v1/ai/batch-predict-intents | prédire plusieurs commentaires |
| GET | /api/v1/ai/model-info | obtenir les informations du modèle |
| GET | /api/v1/ai/model-metrics | obtenir les métriques du modèle |

Ces routes seront protégées avec le même mécanisme que les routes du Bloc 1 :

```text
X-API-Key
```

## 15. Tests prévus

Des tests automatisés seront ajoutés afin de vérifier le bon fonctionnement du service IA.

Tests prévus :

```text
tests/test_ai_dataset.py
tests/test_intent_model.py
tests/test_ai_api.py
```

Ils permettront de vérifier :

- que le dataset NLP existe ;
- que les commentaires vides sont exclus ;
- que les labels attendus sont présents ;
- que les jeux train, validation et test sont créés ;
- que le modèle peut être chargé ;
- que le modèle peut prédire une intention ;
- que les routes API IA sont protégées ;
- que les réponses API respectent le format attendu.

## 16. Monitoring prévu

Le service IA devra produire des informations de monitoring.

Les métriques suivies seront :

- nombre total de prédictions ;
- répartition des intentions prédites ;
- score moyen de confiance ;
- nombre de prédictions à faible confiance ;
- temps moyen de prédiction ;
- version du modèle utilisée.

Les sorties prévues sont :

```text
data/ai/predictions/ai_predictions_log.csv
data/ai/reports/model_monitoring_report.csv
```

Le monitoring permettra de garder une trace des prédictions réalisées par le service IA.

## 17. Contraintes et limites

Le Bloc 2 respecte les contraintes suivantes :

- aucune donnée réelle PayLive n’est utilisée ;
- les commentaires sont simulés ;
- le modèle est entraîné localement ;
- aucune donnée bancaire réelle n’est traitée ;
- aucune décision automatique critique n’est prise ;
- le service IA reste une preuve de concept pédagogique ;
- les prédictions du modèle doivent être interprétées comme une aide à la décision, et non comme une vérité absolue.

Limites de la première version :

- le modèle dépend de la qualité des labels simulés ;
- les commentaires très ambigus peuvent être mal classés ;
- les fautes d’orthographe peuvent réduire la performance ;
- le modèle ne comprend pas toujours le contexte global du live ;
- l’extraction fine du produit, de la taille, de la couleur et de la quantité n’est pas prioritaire dans la première version.

## 18. Évolutions possibles

Après la première version, le service IA pourra évoluer vers :

- l’extraction automatique du produit mentionné ;
- l’extraction de la taille ;
- l’extraction de la couleur ;
- l’extraction de la quantité ;
- l’utilisation d’un modèle transformer ;
- l’utilisation d’un modèle multilingue ;
- l’amélioration du monitoring ;
- l’ajout d’un système de réentraînement ;
- l’ajout d’un retour utilisateur pour corriger les prédictions ;
- l’intégration dans une interface vendeur.

## 19. Critères de réussite du Bloc 2

Le Bloc 2 sera considéré comme réussi si :

- le dataset NLP est généré automatiquement ;
- le dataset est séparé en train, validation et test ;
- un modèle baseline est entraîné ;
- un benchmark de modèles est produit ;
- les métriques d’évaluation sont générées ;
- le modèle entraîné est sauvegardé ;
- le modèle est exposé via une API REST ;
- l’API IA est sécurisée ;
- les tests automatisés passent ;
- un rapport de monitoring est produit ;
- la documentation du Bloc 2 est complète.

## 20. Lien avec le Bloc 1

Le Bloc 2 s’appuie directement sur les résultats du Bloc 1.

Le Bloc 1 a permis de construire :

- les données brutes simulées ;
- les extractions multi-sources ;
- les données nettoyées ;
- le dataset final analytique ;
- la base PostgreSQL ;
- l’API de mise à disposition ;
- les contrôles qualité ;
- les rapports techniques.

Le Bloc 2 réutilise principalement les données nettoyées, en particulier :

```text
data/processed/clean/live_comments_clean.csv
```

Ce fichier devient la base du dataset NLP utilisé pour entraîner le modèle IA.

## 21. Conclusion

Le Bloc 2 du projet **PayLive AI Copilot** vise à intégrer un service IA complet autour de la classification des commentaires de live shopping.

Le premier objectif est de détecter automatiquement l’intention d’un commentaire afin d’aider le vendeur à identifier plus rapidement les messages à valeur commerciale.

Cette étape prépare la suite du projet en transformant le pipeline de données du Bloc 1 en un service IA exploitable par une application.

Le service IA développé dans ce Bloc 2 constituera une première version fonctionnelle, locale, documentée, testée et monitorée du moteur intelligent de PayLive AI Copilot.