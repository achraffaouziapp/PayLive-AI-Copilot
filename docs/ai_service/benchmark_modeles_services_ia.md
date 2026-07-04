# Benchmark des modèles et services IA — PayLive AI Copilot

## 1. Objectif du document

Ce document présente le benchmark des modèles et services IA étudiés dans le cadre du Bloc 2 du projet **PayLive AI Copilot**.

L’objectif est de choisir une approche adaptée pour classifier automatiquement les commentaires de live shopping selon leur intention.

Le benchmark permet de comparer plusieurs solutions selon des critères techniques, fonctionnels, économiques, réglementaires et opérationnels.

## 2. Besoin IA à couvrir

Le service IA doit recevoir un commentaire de live shopping et prédire une intention.

Exemple d’entrée :

```text
je prends le pull rouge en M
```

Sortie attendue :

```text
purchase_intent
```

Classes prévues :

```text
purchase_intent
product_question
payment_question
shipping_question
other
unknown
```

La classe la plus importante pour le besoin métier est :

```text
purchase_intent
```

Elle permet d’identifier les commentaires pouvant déclencher une action commerciale.

## 3. Contraintes du projet

Le choix du modèle doit respecter les contraintes suivantes :

| Contrainte | Description |
|---|---|
| Données | données simulées uniquement |
| Source principale | data/processed/clean/live_comments_clean.csv |
| Langue | commentaires principalement en français |
| Déploiement | local |
| Budget | pas de coût cloud obligatoire |
| Confidentialité | éviter l’envoi de données vers un service externe |
| Explicabilité | modèle facile à expliquer en soutenance |
| Reproductibilité | entraînement relançable localement |
| API | intégration dans FastAPI |
| Tests | compatible avec Pytest |
| Monitoring | prédictions traçables dans des rapports locaux |

## 4. Solutions comparées

Les solutions étudiées sont :

| Solution | Type | Description |
|---|---|---|
| Règles simples | baseline métier | Classification par mots-clés |
| DummyClassifier | baseline ML | Modèle naïf servant de point de comparaison |
| TF-IDF + Logistic Regression | ML classique | Vectorisation texte + modèle linéaire |
| TF-IDF + Linear SVM | ML classique | Modèle linéaire performant sur texte |
| TF-IDF + Random Forest | ML classique | Modèle non linéaire de comparaison |
| Transformer local | NLP avancé | Modèle pré-entraîné local |
| LLM externe | service IA | Modèle appelé via API externe |

## 5. Critères de comparaison

Les critères retenus pour comparer les solutions sont :

| Critère | Description |
|---|---|
| Adéquation fonctionnelle | capacité à prédire correctement l’intention |
| Simplicité | facilité de mise en œuvre |
| Explicabilité | facilité à expliquer le modèle |
| Coût | coût d’utilisation ou d’exploitation |
| Confidentialité | maîtrise des données |
| Performance attendue | qualité potentielle des prédictions |
| Temps d’entraînement | rapidité de mise en œuvre |
| Intégration API | facilité d’intégration dans FastAPI |
| Monitoring | facilité à tracer les prédictions |
| Maintenance | facilité à maintenir et faire évoluer |

## 6. Solution 1 — Règles simples

## 6.1. Principe

Les règles simples consistent à classifier les commentaires à partir de mots-clés.

Exemples :

| Mot ou expression | Classe |
|---|---|
| je prends | purchase_intent |
| je veux | purchase_intent |
| combien | product_question |
| prix | product_question |
| livraison | shipping_question |
| payer | payment_question |
| carte | payment_question |

## 6.2. Avantages

- très simple à mettre en œuvre ;
- très rapide ;
- aucun entraînement nécessaire ;
- très explicable ;
- utile comme baseline métier.

## 6.3. Limites

- fragile face aux fautes d’orthographe ;
- difficile à maintenir ;
- faible capacité de généralisation ;
- risque de faux positifs ;
- ne gère pas bien les formulations ambiguës.

## 6.4. Décision

```text
retenu comme baseline explicative, mais pas comme modèle final
```

Cette approche permettra de comparer les modèles ML à une méthode simple.

## 7. Solution 2 — DummyClassifier

## 7.1. Principe

DummyClassifier est un modèle naïf qui prédit selon une stratégie simple.

Exemples de stratégies :

- classe majoritaire ;
- prédiction aléatoire ;
- distribution stratifiée.

## 7.2. Avantages

- très simple ;
- permet d’obtenir une baseline minimale ;
- utile pour vérifier que les autres modèles font mieux qu’un modèle naïf ;
- rapide à exécuter.

## 7.3. Limites

- aucune compréhension du texte ;
- aucune valeur fonctionnelle réelle ;
- performance faible attendue ;
- uniquement utile pour comparaison.

## 7.4. Décision

```text
retenu uniquement pour le benchmark
```

DummyClassifier ne sera pas utilisé en production ou dans l’API.

## 8. Solution 3 — TF-IDF + Logistic Regression

## 8.1. Principe

Cette approche combine :

```text
TfidfVectorizer
LogisticRegression
```

Le texte est transformé en vecteur numérique avec TF-IDF, puis un modèle de régression logistique prédit la classe d’intention.

## 8.2. Avantages

- simple à comprendre ;
- rapide à entraîner ;
- adapté aux textes courts ;
- compatible avec un dataset limité ;
- permet d’obtenir un score de probabilité ;
- facile à sauvegarder avec joblib ;
- facile à charger dans une API ;
- métriques faciles à expliquer ;
- bonne base pour une preuve de concept.

## 8.3. Limites

- ne comprend pas profondément le contexte ;
- sensible aux mots inconnus ;
- dépend fortement de la qualité du dataset ;
- moins performant qu’un transformer sur des phrases complexes.

## 8.4. Décision

```text
retenu comme modèle principal de la première version
```

C’est le meilleur compromis pour le projet.

## 9. Solution 4 — TF-IDF + Linear SVM

## 9.1. Principe

Cette approche utilise une vectorisation TF-IDF suivie d’un classifieur SVM linéaire.

Les SVM linéaires sont souvent adaptés aux problèmes de classification de texte.

## 9.2. Avantages

- bonne performance attendue sur texte court ;
- robuste sur données vectorisées ;
- adapté aux matrices creuses ;
- souvent compétitif avec la régression logistique.

## 9.3. Limites

- score de confiance moins direct selon la configuration ;
- peut nécessiter une calibration ;
- moins simple à expliquer qu’une régression logistique ;
- intégration légèrement moins directe si l’on veut retourner une probabilité.

## 9.4. Décision

```text
retenu dans le benchmark
```

Il sera comparé au modèle principal.

## 10. Solution 5 — TF-IDF + Random Forest

## 10.1. Principe

Cette approche utilise TF-IDF puis un modèle Random Forest.

Random Forest est un ensemble d’arbres de décision.

## 10.2. Avantages

- modèle robuste ;
- capable de capturer des relations non linéaires ;
- permet une comparaison avec un modèle non linéaire ;
- facile à utiliser avec scikit-learn.

## 10.3. Limites

- moins adapté aux matrices textuelles très creuses ;
- plus lourd que les modèles linéaires ;
- interprétation moins directe ;
- peut être moins performant sur texte que les modèles linéaires.

## 10.4. Décision

```text
retenu comme comparaison secondaire
```

Il ne sera probablement pas le modèle final, mais il enrichit le benchmark.

## 11. Solution 6 — Transformer local

## 11.1. Principe

Un modèle transformer local utilise un modèle pré-entraîné de type BERT, CamemBERT ou DistilBERT.

Ces modèles produisent des représentations plus riches du langage.

## 11.2. Avantages

- meilleure compréhension du contexte ;
- meilleure gestion de formulations variées ;
- potentiellement meilleure performance ;
- adapté aux commentaires ambigus ;
- possibilité de fine-tuning.

## 11.3. Limites

- dépendances plus lourdes ;
- besoin de plus de ressources ;
- temps d’entraînement plus long ;
- complexité supérieure ;
- moins adapté à une première version simple ;
- peut être difficile à justifier si le dataset est petit.

## 11.4. Décision

```text
non retenu pour la première version, mais envisagé comme évolution
```

Le transformer local pourra être ajouté dans une version avancée du projet.

## 12. Solution 7 — LLM externe

## 12.1. Principe

Un LLM externe consiste à appeler un service IA via API afin de classifier le commentaire.

Exemple de prompt :

```text
Classe ce commentaire dans une des catégories suivantes :
purchase_intent, product_question, payment_question, shipping_question, other, unknown.

Commentaire : "je prends le pull rouge en M"
```

## 12.2. Avantages

- très flexible ;
- bonne compréhension du langage ;
- pas forcément besoin d’entraînement local ;
- peut gérer des formulations très variées ;
- utile pour générer des explications.

## 12.3. Limites

- dépendance à un service externe ;
- coût potentiel ;
- gestion des quotas ;
- confidentialité plus sensible ;
- reproductibilité plus difficile ;
- latence réseau ;
- besoin de sécuriser les clés API externes ;
- plus complexe à justifier pour une version locale.

## 12.4. Décision

```text
non retenu pour la première version locale
```

Le projet privilégie un modèle local pour limiter les dépendances et maîtriser les données.

## 13. Tableau comparatif qualitatif

| Solution | Fonctionnel | Simplicité | Explicabilité | Coût | Confidentialité | Intégration API |
|---|---|---|---|---|---|---|
| Règles simples | moyen | très élevée | très élevée | nul | très bonne | très simple |
| DummyClassifier | faible | très élevée | élevée | nul | très bonne | simple |
| TF-IDF + Logistic Regression | bon | élevée | bonne | nul | très bonne | simple |
| TF-IDF + Linear SVM | bon | moyenne | moyenne | nul | très bonne | moyenne |
| TF-IDF + Random Forest | moyen | moyenne | moyenne | nul | très bonne | moyenne |
| Transformer local | très bon potentiel | faible | moyenne | variable | bonne | moyenne |
| LLM externe | très bon potentiel | moyenne | faible à moyenne | variable | plus sensible | moyenne |

## 14. Tableau de scoring

Notation de 1 à 5.

| Solution | Fonctionnel | Simplicité | Explicabilité | Coût | Confidentialité | Intégration | Score total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Règles simples | 2 | 5 | 5 | 5 | 5 | 5 | 27 |
| DummyClassifier | 1 | 5 | 5 | 5 | 5 | 5 | 26 |
| TF-IDF + Logistic Regression | 4 | 5 | 4 | 5 | 5 | 5 | 28 |
| TF-IDF + Linear SVM | 4 | 4 | 3 | 5 | 5 | 4 | 25 |
| TF-IDF + Random Forest | 3 | 3 | 3 | 5 | 5 | 4 | 23 |
| Transformer local | 5 | 2 | 3 | 4 | 5 | 3 | 22 |
| LLM externe | 5 | 4 | 2 | 2 | 2 | 4 | 19 |

## 15. Classement final

| Rang | Solution | Décision |
|---:|---|---|
| 1 | TF-IDF + Logistic Regression | modèle principal |
| 2 | TF-IDF + Linear SVM | modèle comparatif |
| 3 | Règles simples | baseline métier |
| 4 | DummyClassifier | baseline ML |
| 5 | TF-IDF + Random Forest | comparaison secondaire |
| 6 | Transformer local | évolution possible |
| 7 | LLM externe | évolution possible non prioritaire |

## 16. Solution retenue

La solution retenue pour la première version du service IA est :

```text
TF-IDF + Logistic Regression
```

Justification :

- répond au besoin de classification ;
- fonctionne localement ;
- ne nécessite pas de service externe ;
- limite les risques de confidentialité ;
- s’intègre facilement dans FastAPI ;
- peut être testé automatiquement ;
- produit des métriques simples à expliquer ;
- reste adapté à un projet étudiant ;
- permet une soutenance claire.

## 17. Modèle final prévu

Pipeline prévu :

```text
comment_text
    ↓
TfidfVectorizer
    ↓
LogisticRegression
    ↓
predicted_intent + confidence_score
```

Artefacts sauvegardés :

```text
models/intent_classifier/model.joblib
models/intent_classifier/vectorizer.joblib
models/intent_classifier/label_encoder.joblib
models/intent_classifier/model_metadata.json
```

## 18. Benchmark expérimental prévu

Le benchmark théorique sera complété par un benchmark expérimental.

Script prévu :

```text
src/ai/training/benchmark_intent_models.py
```

Sortie attendue :

```text
data/ai/reports/model_benchmark_report.csv
```

Métriques du benchmark :

- accuracy ;
- precision macro ;
- recall macro ;
- f1-score macro ;
- temps d’entraînement ;
- temps de prédiction ;
- modèle sélectionné ou non.

## 19. Critères de sélection finale

Le modèle final sera choisi selon :

- f1-score global ;
- performance sur la classe purchase_intent ;
- simplicité d’intégration ;
- stabilité des prédictions ;
- facilité de sauvegarde ;
- compatibilité avec l’API ;
- lisibilité en soutenance.

Si les performances sont proches, le modèle le plus simple sera privilégié.

## 20. Limites du benchmark

Le benchmark présente certaines limites :

- dataset simulé ;
- taille limitée des données ;
- labels générés automatiquement ;
- absence de commentaires réels PayLive ;
- absence de bruit réel issu de TikTok ou Instagram ;
- pas de mesure en production réelle.

Ces limites sont acceptées car le projet est une preuve de concept pédagogique.

## 21. Évolutions possibles

Évolutions futures :

- enrichir le dataset avec plus de variations ;
- ajouter des fautes d’orthographe simulées ;
- tester un modèle transformer local ;
- tester un modèle multilingue ;
- comparer avec un LLM externe ;
- ajouter une phase de correction humaine ;
- réentraîner régulièrement le modèle ;
- mesurer le drift des prédictions.

## 22. Conclusion

Le benchmark montre que **TF-IDF + Logistic Regression** est le meilleur compromis pour la première version du service IA.

Cette solution est locale, simple, testable, explicable et adaptée au besoin de classification des commentaires.

Elle permet de construire une première version fonctionnelle du moteur IA de **PayLive AI Copilot**, tout en gardant des perspectives d’évolution vers des modèles plus avancés.
