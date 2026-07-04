# Benchmark des modèles et services IA — PayLive AI Copilot

## 1. Objectif du document

Ce document présente le benchmark des modèles et services IA étudiés dans le cadre du Bloc 2 du projet **PayLive AI Copilot**.

L’objectif est de choisir une approche adaptée pour classifier automatiquement les commentaires de live shopping selon leur intention.

Le benchmark permet de comparer plusieurs solutions selon des critères :

- techniques ;
- fonctionnels ;
- économiques ;
- réglementaires ;
- opérationnels ;
- environnementaux.

Ce document couvre deux niveaux de comparaison :

1. un benchmark de modèles internes entraînés localement ;
2. un benchmark de services IA existants disponibles sur le marché.

L’objectif final est de justifier le choix de la solution retenue pour la première version du service IA.

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

Le choix du modèle ou du service IA doit respecter les contraintes suivantes :

| Contrainte | Description |
|---|---|
| Données | données simulées uniquement |
| Source principale | `data/processed/clean/live_comments_clean.csv` |
| Langue | commentaires principalement en français |
| Déploiement | local |
| Budget | pas de coût cloud obligatoire |
| Confidentialité | éviter l’envoi de données vers un service externe |
| Explicabilité | modèle facile à expliquer en soutenance |
| Reproductibilité | entraînement relançable localement |
| API | intégration dans FastAPI |
| Tests | compatible avec Pytest |
| Monitoring | prédictions traçables dans des rapports locaux |
| Maintenance | solution compréhensible et maintenable |
| Éco-responsabilité | privilégier une solution sobre et adaptée au besoin |

## 4. Solutions comparées

Les solutions étudiées sont réparties en deux catégories :

1. les modèles internes ;
2. les services IA externes ou cloud.

### 4.1. Modèles internes étudiés

| Solution | Type | Description |
|---|---|---|
| Règles simples | baseline métier | classification par mots-clés |
| DummyClassifier | baseline ML | modèle naïf servant de point de comparaison |
| TF-IDF + Logistic Regression | ML classique | vectorisation texte + modèle linéaire |
| TF-IDF + Linear SVM | ML classique | modèle linéaire performant sur texte |
| TF-IDF + Multinomial Naive Bayes | ML classique | modèle probabiliste souvent utilisé sur texte |
| TF-IDF + Random Forest | ML classique | modèle non linéaire de comparaison |
| Transformer local | NLP avancé | modèle pré-entraîné local |
| LLM externe | service IA | modèle appelé via API externe |

### 4.2. Services IA externes étudiés

| Solution | Type | Description |
|---|---|---|
| Modèle local scikit-learn | modèle local | modèle entraîné localement avec TF-IDF + Logistic Regression |
| Hugging Face local | modèle local avancé | utilisation possible d’un modèle transformer local |
| Hugging Face Inference Providers | service IA externe | accès à plusieurs modèles via des fournisseurs d’inférence |
| OpenAI API | service IA externe | utilisation d’un LLM via API pour classifier les commentaires |
| Google Cloud Natural Language / Vertex AI | service cloud IA | services Google Cloud pour NLP, classification ou modèles IA |
| Azure AI Language / Azure OpenAI | service cloud IA | services Microsoft pour NLP ou modèles génératifs |
| AWS Comprehend | service cloud NLP | service AWS pour analyse NLP et classification personnalisée |

## 5. Critères de comparaison

Les critères retenus pour comparer les solutions sont :

| Critère | Description |
|---|---|
| Adéquation fonctionnelle | capacité à prédire correctement l’intention |
| Simplicité | facilité de mise en œuvre |
| Explicabilité | facilité à expliquer le modèle ou le service |
| Coût | coût d’utilisation, d’entraînement ou d’inférence |
| Confidentialité | maîtrise des données et limitation des envois externes |
| Performance attendue | qualité potentielle des prédictions |
| Temps d’entraînement | rapidité de mise en œuvre |
| Intégration API | facilité d’intégration dans FastAPI |
| Monitoring | facilité à tracer les prédictions |
| Maintenance | facilité à maintenir et faire évoluer |
| Prérequis | comptes, clés API, ressources machine ou cloud nécessaires |
| Éco-responsabilité | sobriété de la solution en ressources et appels externes |

## 6. Benchmark des modèles internes

## 6.1. Solution 1 — Règles simples

### 6.1.1. Principe

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

### 6.1.2. Avantages

- très simple à mettre en œuvre ;
- très rapide ;
- aucun entraînement nécessaire ;
- très explicable ;
- utile comme baseline métier.

### 6.1.3. Limites

- fragile face aux fautes d’orthographe ;
- difficile à maintenir ;
- faible capacité de généralisation ;
- risque de faux positifs ;
- ne gère pas bien les formulations ambiguës.

### 6.1.4. Décision

```text
retenu comme baseline explicative, mais pas comme modèle final
```

Cette approche permet de comparer les modèles ML à une méthode simple.

## 6.2. Solution 2 — DummyClassifier

### 6.2.1. Principe

DummyClassifier est un modèle naïf qui prédit selon une stratégie simple.

Exemples de stratégies :

- classe majoritaire ;
- prédiction aléatoire ;
- distribution stratifiée.

Dans le projet, il sert de baseline minimale.

### 6.2.2. Avantages

- très simple ;
- permet d’obtenir une baseline minimale ;
- utile pour vérifier que les autres modèles font mieux qu’un modèle naïf ;
- rapide à exécuter.

### 6.2.3. Limites

- aucune compréhension du texte ;
- aucune valeur fonctionnelle réelle ;
- performance faible attendue ;
- uniquement utile pour comparaison.

### 6.2.4. Décision

```text
retenu uniquement pour le benchmark
```

DummyClassifier ne sera pas utilisé dans l’API comme modèle final.

## 6.3. Solution 3 — TF-IDF + Logistic Regression

### 6.3.1. Principe

Cette approche combine :

```text
TfidfVectorizer
LogisticRegression
```

Le texte est transformé en vecteur numérique avec TF-IDF, puis un modèle de régression logistique prédit la classe d’intention.

### 6.3.2. Avantages

- simple à comprendre ;
- rapide à entraîner ;
- adapté aux textes courts ;
- compatible avec un dataset limité ;
- permet d’obtenir un score de probabilité ;
- facile à sauvegarder avec `joblib` ;
- facile à charger dans une API ;
- métriques faciles à expliquer ;
- bonne base pour une preuve de concept.

### 6.3.3. Limites

- ne comprend pas profondément le contexte ;
- sensible aux mots inconnus ;
- dépend fortement de la qualité du dataset ;
- moins performant qu’un transformer sur des phrases complexes.

### 6.3.4. Décision

```text
retenu comme modèle principal de la première version
```

C’est le meilleur compromis pour le projet.

## 6.4. Solution 4 — TF-IDF + Linear SVM

### 6.4.1. Principe

Cette approche utilise une vectorisation TF-IDF suivie d’un classifieur SVM linéaire.

Les SVM linéaires sont souvent adaptés aux problèmes de classification de texte.

### 6.4.2. Avantages

- bonne performance attendue sur texte court ;
- robuste sur données vectorisées ;
- adapté aux matrices creuses ;
- souvent compétitif avec la régression logistique.

### 6.4.3. Limites

- score de confiance moins direct selon la configuration ;
- peut nécessiter une calibration ;
- moins simple à expliquer qu’une régression logistique ;
- intégration légèrement moins directe si l’on veut retourner une probabilité.

### 6.4.4. Décision

```text
retenu dans le benchmark
```

Il est comparé au modèle principal.

## 6.5. Solution 5 — TF-IDF + Multinomial Naive Bayes

### 6.5.1. Principe

Cette approche utilise TF-IDF puis un modèle Multinomial Naive Bayes.

Ce modèle est souvent utilisé pour des tâches de classification de texte.

### 6.5.2. Avantages

- rapide à entraîner ;
- simple à utiliser ;
- adapté aux données textuelles vectorisées ;
- faible coût de calcul ;
- bon modèle comparatif.

### 6.5.3. Limites

- hypothèse d’indépendance entre les variables ;
- performance parfois inférieure aux modèles linéaires modernes ;
- moins robuste sur certaines formulations ambiguës.

### 6.5.4. Décision

```text
retenu dans le benchmark comme modèle comparatif
```

## 6.6. Solution 6 — TF-IDF + Random Forest

### 6.6.1. Principe

Cette approche utilise TF-IDF puis un modèle Random Forest.

Random Forest est un ensemble d’arbres de décision.

### 6.6.2. Avantages

- modèle robuste ;
- capable de capturer des relations non linéaires ;
- permet une comparaison avec un modèle non linéaire ;
- facile à utiliser avec scikit-learn.

### 6.6.3. Limites

- moins adapté aux matrices textuelles très creuses ;
- plus lourd que les modèles linéaires ;
- interprétation moins directe ;
- peut être moins performant sur texte que les modèles linéaires.

### 6.6.4. Décision

```text
retenu comme comparaison secondaire
```

Il ne sera probablement pas le modèle final, mais il enrichit le benchmark.

## 6.7. Solution 7 — Transformer local

### 6.7.1. Principe

Un modèle transformer local utilise un modèle pré-entraîné de type BERT, CamemBERT ou DistilBERT.

Ces modèles produisent des représentations plus riches du langage.

### 6.7.2. Avantages

- meilleure compréhension du contexte ;
- meilleure gestion de formulations variées ;
- potentiellement meilleure performance ;
- adapté aux commentaires ambigus ;
- possibilité de fine-tuning.

### 6.7.3. Limites

- dépendances plus lourdes ;
- besoin de plus de ressources ;
- temps d’entraînement plus long ;
- complexité supérieure ;
- moins adapté à une première version simple ;
- peut être difficile à justifier si le dataset est petit.

### 6.7.4. Décision

```text
non retenu pour la première version, mais envisagé comme évolution
```

Le transformer local pourra être ajouté dans une version avancée du projet.

## 6.8. Solution 8 — LLM externe

### 6.8.1. Principe

Un LLM externe consiste à appeler un service IA via API afin de classifier le commentaire.

Exemple de prompt :

```text
Classe ce commentaire dans une des catégories suivantes :
purchase_intent, product_question, payment_question, shipping_question, other, unknown.

Commentaire : "je prends le pull rouge en M"
```

### 6.8.2. Avantages

- très flexible ;
- bonne compréhension du langage ;
- pas forcément besoin d’entraînement local ;
- peut gérer des formulations très variées ;
- utile pour générer des explications.

### 6.8.3. Limites

- dépendance à un service externe ;
- coût potentiel ;
- gestion des quotas ;
- confidentialité plus sensible ;
- reproductibilité plus difficile ;
- latence réseau ;
- besoin de sécuriser les clés API externes ;
- plus complexe à justifier pour une version locale.

### 6.8.4. Décision

```text
non retenu pour la première version locale
```

Le projet privilégie un modèle local pour limiter les dépendances et maîtriser les données.

## 7. Tableau comparatif qualitatif des modèles internes

| Solution | Fonctionnel | Simplicité | Explicabilité | Coût | Confidentialité | Intégration API |
|---|---|---|---|---|---|---|
| Règles simples | moyen | très élevée | très élevée | nul | très bonne | très simple |
| DummyClassifier | faible | très élevée | élevée | nul | très bonne | simple |
| TF-IDF + Logistic Regression | bon | élevée | bonne | nul | très bonne | simple |
| TF-IDF + Linear SVM | bon | moyenne | moyenne | nul | très bonne | moyenne |
| TF-IDF + Multinomial Naive Bayes | moyen à bon | élevée | moyenne | nul | très bonne | simple |
| TF-IDF + Random Forest | moyen | moyenne | moyenne | nul | très bonne | moyenne |
| Transformer local | très bon potentiel | faible | moyenne | variable | bonne | moyenne |
| LLM externe | très bon potentiel | moyenne | faible à moyenne | variable | plus sensible | moyenne |

## 8. Tableau de scoring des modèles internes

Notation de 1 à 5.

| Solution | Fonctionnel | Simplicité | Explicabilité | Coût | Confidentialité | Intégration | Score total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Règles simples | 2 | 5 | 5 | 5 | 5 | 5 | 27 |
| DummyClassifier | 1 | 5 | 5 | 5 | 5 | 5 | 26 |
| TF-IDF + Logistic Regression | 4 | 5 | 4 | 5 | 5 | 5 | 28 |
| TF-IDF + Linear SVM | 4 | 4 | 3 | 5 | 5 | 4 | 25 |
| TF-IDF + Multinomial Naive Bayes | 3 | 5 | 3 | 5 | 5 | 5 | 26 |
| TF-IDF + Random Forest | 3 | 3 | 3 | 5 | 5 | 4 | 23 |
| Transformer local | 5 | 2 | 3 | 4 | 5 | 3 | 22 |
| LLM externe | 5 | 4 | 2 | 2 | 2 | 4 | 19 |

## 9. Benchmark expérimental interne

Le benchmark théorique est complété par un benchmark expérimental.

Script utilisé :

```text
src/ai/training/benchmark_intent_models.py
```

Sorties générées :

```text
data/ai/reports/model_benchmark_report.csv
data/ai/reports/model_benchmark_classification_report.csv
data/ai/reports/model_benchmark_selection_report.csv
```

Modèles comparés dans le script :

```text
business_rules_baseline
dummy_most_frequent
tfidf_logistic_regression
tfidf_linear_svm
tfidf_multinomial_nb
tfidf_random_forest
```

Métriques produites :

- accuracy ;
- precision macro ;
- recall macro ;
- f1-score macro ;
- f1-score pondéré ;
- score moyen de confiance ;
- temps d’entraînement ;
- temps de prédiction ;
- modèle éligible ou non à la sélection finale.

## 10. Résultat du benchmark expérimental

Le benchmark interne a sélectionné le modèle suivant :

```text
tfidf_logistic_regression
```

Résultats observés sur le jeu de validation :

```text
validation_accuracy      = 0.8
validation_macro_f1      = 0.6667
validation_weighted_f1   = 0.7333
```

Ce résultat confirme que le choix initial de **TF-IDF + Logistic Regression** est cohérent.

## 11. Classement final des modèles internes

| Rang | Solution | Décision |
|---:|---|---|
| 1 | TF-IDF + Logistic Regression | modèle principal |
| 2 | TF-IDF + Linear SVM | modèle comparatif |
| 3 | TF-IDF + Multinomial Naive Bayes | modèle comparatif |
| 4 | Règles simples | baseline métier |
| 5 | DummyClassifier | baseline ML |
| 6 | TF-IDF + Random Forest | comparaison secondaire |
| 7 | Transformer local | évolution possible |
| 8 | LLM externe | évolution possible non prioritaire |

## 12. Benchmark complémentaire des services IA existants

## 12.1. Objectif du benchmark de services IA

En complément du benchmark interne des modèles de classification, un benchmark de services IA existants a été réalisé.

L’objectif est de comparer plusieurs solutions possibles pour répondre au besoin du projet :

```text
classifier automatiquement les commentaires de live shopping selon leur intention
```

Ce benchmark permet de justifier pourquoi la première version du projet utilise un modèle local entraîné avec scikit-learn, plutôt qu’un service IA externe.

## 12.2. Services et solutions comparés

| Solution | Type | Description |
|---|---|---|
| Modèle local scikit-learn | modèle local | modèle entraîné localement avec TF-IDF + Logistic Regression |
| Hugging Face local | modèle local avancé | utilisation possible d’un modèle NLP transformer local |
| Hugging Face Inference Providers | service IA externe | accès à plusieurs modèles via des fournisseurs d’inférence |
| OpenAI API | service IA externe | utilisation d’un LLM via API pour classifier les commentaires |
| Google Cloud Natural Language / Vertex AI | service cloud IA | services Google Cloud pour NLP, classification ou modèles IA |
| Azure AI Language / Azure OpenAI | service cloud IA | services Microsoft pour NLP ou modèles génératifs |
| AWS Comprehend | service cloud NLP | service AWS pour analyse NLP et classification personnalisée |

## 12.3. Critères de comparaison des services IA

Les services IA sont comparés selon les critères suivants :

| Critère | Description |
|---|---|
| Fonctionnalités | capacité à répondre au besoin de classification |
| Contraintes techniques | complexité d’installation, API, dépendances, cloud |
| Coût | coût d’appel API, d’entraînement, d’hébergement ou d’inférence |
| Limites | limites fonctionnelles, techniques ou opérationnelles |
| Prérequis | compte cloud, clé API, facturation, ressources machine |
| Confidentialité | niveau d’exposition des données |
| Dépendance externe | dépendance à un fournisseur ou à Internet |
| Intégration | facilité d’intégration dans FastAPI |
| Monitoring | possibilité de suivre les prédictions ou l’usage |
| Éco-responsabilité | sobriété de la solution par rapport au besoin réel |

## 12.4. Tableau comparatif des services IA

| Solution | Fonctionnalités | Contraintes techniques | Coût | Limites | Prérequis | Éco-responsabilité | Décision |
|---|---|---|---|---|---|---|---|
| Modèle local scikit-learn | Classification supervisée locale | Nécessite un dataset labellisé et un entraînement local | Très faible, pas d’appel API payant | Moins performant qu’un modèle avancé sur textes ambigus | Python, scikit-learn, dataset NLP | Solution légère, peu de ressources, pas d’appel cloud | **Retenu** |
| Hugging Face local | Modèles NLP avancés, transformers | Installation plus lourde, besoin de ressources CPU/GPU selon modèle | Gratuit hors coût machine | Plus complexe à entraîner et intégrer | `transformers`, `torch`, modèle pré-entraîné | Plus coûteux en ressources qu’un modèle classique | Écarté pour V1, évolution possible |
| Hugging Face Inference Providers | Accès à des modèles via API | Dépendance à un fournisseur externe | Paiement à l’usage selon fournisseur | Données envoyées à un service externe, dépendance réseau | Compte Hugging Face, clé API | Mutualisation cloud mais appels externes | Écarté pour V1 |
| OpenAI API | Classification possible par prompt ou appel de modèle | Dépendance API, gestion prompts, clé API, quotas | Coût variable selon modèle et volume de tokens | Données envoyées à un tiers, coût récurrent, reproductibilité plus difficile | Compte API, clé, gestion sécurité | Modèles puissants mais surdimensionnés pour une tâche simple | Écarté pour V1 |
| Google Cloud Natural Language / Vertex AI | NLP cloud, classification, modèles IA | Configuration cloud, IAM, projet GCP | Coût selon usage, caractères, modèles ou ressources | Plus complexe qu’une preuve de concept locale | Compte Google Cloud, facturation, configuration IAM | Infrastructure cloud potentiellement excessive pour V1 | Écarté pour V1 |
| Azure AI Language / Azure OpenAI | Services NLP et modèles IA via Azure | Configuration Azure, ressources, clés, endpoints | Coût selon service et consommation | Dépendance cloud, cycle de vie des services à surveiller | Compte Azure, ressource IA, sécurité | Solution cloud plus lourde que nécessaire pour V1 | Écarté pour V1 |
| AWS Comprehend | NLP cloud, classification personnalisée | Configuration AWS, entraînement custom, IAM | Coûts d’entraînement, gestion du modèle et inférence | Moins adapté au projet local, coût et configuration plus élevés | Compte AWS, données labellisées, IAM | Infrastructure cloud utile en production mais excessive ici | Écarté pour V1 |

## 13. Analyse détaillée des services IA

## 13.1. Modèle local scikit-learn

La solution locale repose sur :

```text
TF-IDF + Logistic Regression
```

Elle est adaptée au projet car :

- elle fonctionne localement ;
- elle ne nécessite pas de service externe ;
- elle ne génère pas de coût API ;
- elle est rapide à entraîner ;
- elle est simple à expliquer ;
- elle est suffisante pour une première version ;
- elle s’intègre facilement dans FastAPI ;
- elle permet de sauvegarder les artefacts du modèle avec `joblib`.

Limites :

- compréhension limitée du contexte ;
- performance dépendante de la qualité du dataset ;
- robustesse limitée face aux phrases très ambiguës ;
- moins performante qu’un modèle transformer sur du langage complexe.

Décision :

```text
retenu pour la première version du service IA
```

## 13.2. Hugging Face local

Une solution possible serait d’utiliser un modèle transformer local, par exemple un modèle francophone ou multilingue.

Avantages :

- meilleure compréhension du langage ;
- meilleure robustesse aux formulations variées ;
- possibilité d’améliorer la performance sur des textes ambigus ;
- pas d’envoi de données vers un service externe si le modèle est exécuté localement.

Limites :

- dépendances plus lourdes ;
- temps d’entraînement plus élevé ;
- ressources machine plus importantes ;
- complexité plus élevée pour le projet ;
- moins adapté à une première version rapide et explicable.

Décision :

```text
écarté pour la première version, mais conservé comme évolution possible
```

## 13.3. Hugging Face Inference Providers

Hugging Face Inference Providers permet d’accéder à différents modèles via des fournisseurs d’inférence.

Avantages :

- accès rapide à des modèles avancés ;
- pas besoin d’héberger soi-même le modèle ;
- intégration possible via API ;
- choix large de modèles.

Limites :

- dépendance externe ;
- coût selon l’usage ;
- besoin de gérer les clés API ;
- envoi potentiel de commentaires vers un service tiers ;
- moins de contrôle sur l’infrastructure.

Décision :

```text
écarté pour la première version afin de garder une solution locale et maîtrisée
```

## 13.4. OpenAI API

OpenAI API pourrait être utilisée pour classifier les commentaires via prompt, par exemple en demandant au modèle de choisir une intention parmi une liste.

Avantages :

- très bonne compréhension du langage naturel ;
- capacité à gérer des commentaires ambigus ;
- pas besoin d’entraîner un modèle local ;
- flexibilité importante ;
- possibilité d’ajouter des explications ou de l’extraction avancée.

Limites :

- coût récurrent ;
- dépendance à une API externe ;
- gestion des clés API ;
- difficulté à garantir une reproductibilité parfaite ;
- envoi potentiel des commentaires vers un service tiers ;
- solution surdimensionnée pour une première classification simple.

Décision :

```text
écarté pour la première version, envisageable plus tard pour enrichir le Copilot
```

## 13.5. Google Cloud Natural Language / Vertex AI

Google Cloud propose des services NLP et IA permettant d’analyser du texte ou d’exploiter des modèles via une infrastructure cloud.

Avantages :

- infrastructure cloud robuste ;
- services managés ;
- possibilité d’évoluer vers des modèles plus avancés ;
- intégration possible dans une architecture cloud.

Limites :

- configuration cloud plus lourde ;
- besoin d’un compte Google Cloud ;
- gestion IAM et facturation ;
- coût selon usage ;
- moins adapté à un projet local étudiant ;
- dépendance fournisseur.

Décision :

```text
écarté pour la première version
```

## 13.6. Azure AI Language / Azure OpenAI

Azure propose des services IA pour le langage et des services de modèles génératifs.

Avantages :

- intégration cloud entreprise ;
- sécurité et gestion des accès avancées ;
- services adaptés à des environnements professionnels ;
- possibilité d’utiliser des modèles génératifs.

Limites :

- complexité de configuration ;
- coût selon service ;
- dépendance cloud ;
- surdimensionné pour la preuve de concept ;
- cycle de vie des services Azure à surveiller.

Décision :

```text
écarté pour la première version
```

## 13.7. AWS Comprehend

AWS Comprehend est un service NLP managé qui peut être utilisé pour analyser du texte et créer des modèles personnalisés de classification.

Avantages :

- service NLP managé ;
- intégration possible dans un environnement AWS ;
- adapté à des cas d’usage professionnels ;
- possibilité de classification personnalisée.

Limites :

- configuration AWS plus lourde ;
- gestion IAM ;
- coût d’entraînement et d’inférence ;
- dépendance cloud ;
- moins adapté à une preuve de concept locale.

Décision :

```text
écarté pour la première version
```

## 14. Tableau de scoring des services IA

Notation de 1 à 5.

| Solution | Fonctionnel | Simplicité | Coût | Confidentialité | Intégration | Éco-responsabilité | Score total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Modèle local scikit-learn | 4 | 5 | 5 | 5 | 5 | 5 | 29 |
| Hugging Face local | 5 | 3 | 4 | 5 | 3 | 3 | 23 |
| Hugging Face Inference Providers | 5 | 4 | 3 | 3 | 4 | 3 | 22 |
| OpenAI API | 5 | 4 | 3 | 2 | 4 | 2 | 20 |
| Google Cloud Natural Language / Vertex AI | 4 | 3 | 3 | 3 | 3 | 3 | 19 |
| Azure AI Language / Azure OpenAI | 4 | 3 | 3 | 3 | 3 | 3 | 19 |
| AWS Comprehend | 4 | 3 | 3 | 3 | 3 | 3 | 19 |

## 15. Justification du choix final

La solution retenue pour la première version est :

```text
modèle local scikit-learn — TF-IDF + Logistic Regression
```

Ce choix est justifié par les éléments suivants :

- le modèle répond au besoin principal de classification ;
- il fonctionne localement ;
- il ne nécessite pas de compte cloud ;
- il ne génère pas de coût API ;
- il limite l’exposition des données ;
- il est rapide à entraîner ;
- il est facilement testable ;
- il est simple à intégrer dans FastAPI ;
- il est compatible avec une logique MLOps légère ;
- il est cohérent avec une démarche éco-responsable car il évite l’utilisation d’un grand modèle externe pour une tâche simple ;
- il permet une explication claire en soutenance.

## 16. Services écartés et justification

| Service écarté | Justification |
|---|---|
| Hugging Face local | intéressant mais plus lourd pour une première version |
| Hugging Face Inference Providers | dépendance externe et coût d’usage |
| OpenAI API | très performant mais coût, dépendance API et confidentialité à prendre en compte |
| Google Cloud Natural Language / Vertex AI | configuration cloud plus lourde que nécessaire |
| Azure AI Language / Azure OpenAI | surdimensionné pour la V1 et dépendance cloud |
| AWS Comprehend | configuration et coût moins adaptés au contexte étudiant local |

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

## 18. Intégration prévue dans l’API

Le modèle final est exposé via l’API FastAPI existante.

Routes IA :

```text
POST /api/v1/ai/predict-intent
POST /api/v1/ai/batch-predict-intents
GET  /api/v1/ai/model-info
GET  /api/v1/ai/model-metrics
```

Le modèle est chargé via :

```text
src/ai/inference/intent_predictor.py
```

La couche de service API est située dans :

```text
api/ai_service.py
```

Les routes FastAPI sont situées dans :

```text
api/routes/ai.py
```

## 19. Critères de sélection finale

Le modèle final est choisi selon :

- f1-score global ;
- performance sur la classe `purchase_intent` ;
- simplicité d’intégration ;
- stabilité des prédictions ;
- facilité de sauvegarde ;
- compatibilité avec l’API ;
- score de confiance disponible ;
- lisibilité en soutenance ;
- coût d’exploitation ;
- maîtrise des données ;
- sobriété technique.

Si les performances sont proches, le modèle le plus simple et le plus maîtrisable est privilégié.

## 20. Limites du benchmark

Le benchmark présente certaines limites :

- dataset simulé ;
- taille limitée des données ;
- labels générés automatiquement puis consolidés ;
- absence de commentaires réels PayLive ;
- absence de bruit réel issu de TikTok ou Instagram ;
- pas de mesure en production réelle ;
- pas de test à grande échelle ;
- coûts cloud non mesurés en usage réel ;
- performances évaluées sur une preuve de concept locale.

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
- mesurer le drift des prédictions ;
- ajouter un tableau de bord de monitoring ;
- ajouter des alertes sur les faibles confiances ;
- tester une intégration cloud dans une version production.

## 22. Sources utilisées pour le benchmark

Sources principales consultées :

```text
scikit-learn — TfidfVectorizer
https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

scikit-learn — LogisticRegression
https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

scikit-learn — DummyClassifier
https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html

scikit-learn — LinearSVC
https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html

scikit-learn — RandomForestClassifier
https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

scikit-learn — MultinomialNB
https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html

Hugging Face — Inference Providers
https://huggingface.co/docs/inference-providers/index

Hugging Face — Pricing and Billing
https://huggingface.co/docs/inference-providers/pricing

OpenAI — API Platform
https://openai.com/api/

OpenAI — API Pricing
https://developers.openai.com/api/docs/pricing

Google Cloud — Natural Language Pricing
https://cloud.google.com/natural-language/pricing

Azure OpenAI — Pricing
https://azure.microsoft.com/en-us/pricing/details/azure-openai/

Azure AI Language — Model Lifecycle
https://learn.microsoft.com/en-us/azure/ai-services/language-service/concepts/model-lifecycle

AWS — Amazon Comprehend Pricing
https://aws.amazon.com/comprehend/pricing/
```

## 23. Conclusion

Le benchmark montre que plusieurs modèles et services IA auraient pu répondre au besoin fonctionnel.

Cependant, pour la première version du projet **PayLive AI Copilot**, le modèle local :

```text
TF-IDF + Logistic Regression
```

représente le meilleur compromis entre :

- fonctionnalité ;
- simplicité ;
- coût ;
- confidentialité ;
- intégration technique ;
- sobriété ;
- maintenabilité ;
- explicabilité.

Les services cloud et les LLM externes sont écartés pour la première version, mais restent pertinents comme évolutions possibles si le projet devait passer à une version plus avancée ou à un contexte de production.

Le choix final est donc cohérent avec les contraintes du projet, le besoin métier, la soutenance et la logique pédagogique du Bloc 2.