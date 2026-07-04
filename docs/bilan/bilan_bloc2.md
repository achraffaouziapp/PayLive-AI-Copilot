# Bilan final du Bloc 2 — Service IA PayLive AI Copilot

## 1. Objectif du Bloc 2

Le Bloc 2 du projet **PayLive AI Copilot** avait pour objectif d’intégrer un service d’intelligence artificielle capable d’analyser des commentaires de live shopping et de prédire l’intention exprimée par l’utilisateur.

Le besoin fonctionnel principal était :

```text
détecter automatiquement les commentaires qui expriment une intention d’achat
```

Exemple :

```text
Commentaire : "je prends la robe noire en M"
Résultat attendu : purchase_intent
```

Le service IA devait être intégré dans l’architecture existante du projet, exposé via une API REST, sécurisé, testé, monitoré et documenté.

## 2. Périmètre réalisé

Le Bloc 2 couvre les éléments suivants :

```text
veille technique et réglementaire liée à l’IA
benchmark de modèles et services IA
préparation d’un dataset NLP
entraînement d’un modèle de classification d’intention
évaluation du modèle
benchmark expérimental interne
sauvegarde des artefacts du modèle
module d’inférence
API REST IA avec FastAPI
authentification par X-API-Key
tests automatisés IA/API
journalisation des prédictions
monitoring du modèle
dashboard HTML de monitoring
fichier d’alertes CSV
pipeline GitHub Actions dans une logique MLOps
documentation technique Bloc 2
```

## 3. Besoin IA reformulé

Le service IA reçoit un commentaire de live shopping et prédit une intention parmi plusieurs classes :

```text
purchase_intent
product_question
payment_question
shipping_question
other
unknown
```

La classe prioritaire est `purchase_intent`, car elle permet d’identifier les commentaires pouvant déclencher une action commerciale.

## 4. Données utilisées

Le projet n’utilise aucune donnée réelle de l’entreprise PayLive.

Les données du Bloc 2 sont :

```text
simulées
fictives
pseudonymisées
générées à partir du socle Bloc 1
enrichies avec des exemples contrôlés
```

Fichiers principaux :

```text
data/ai/datasets/comments_intent_dataset.csv
data/ai/datasets/train.csv
data/ai/datasets/validation.csv
data/ai/datasets/test.csv
```

## 5. Préparation du dataset NLP

La préparation du dataset NLP est réalisée par :

```text
src/ai/data_preparation/prepare_nlp_dataset.py
```

Ce script permet de :

```text
charger les commentaires nettoyés du Bloc 1
normaliser les textes
consolider les labels d’intention
ajouter des exemples contrôlés
équilibrer les classes principales
séparer les données en train, validation et test
générer des rapports qualité
```

Rapports générés :

```text
data/ai/reports/nlp_dataset_quality_report.csv
data/ai/reports/train_validation_test_split_report.csv
```

## 6. Veille technique et réglementaire

La veille est documentée dans :

```text
docs/07_ai_service/23_veille_technique_reglementaire_ia.md
```

Thématiques couvertes :

```text
NLP et classification de texte
modèles IA classiques
services IA externes
API IA
sécurité API
OpenAPI
RGPD
AI Act
MLOps léger
monitoring IA
```

Sources utilisées :

```text
documentation scikit-learn
documentation FastAPI
OpenAPI Initiative
CNIL
EUR-Lex
OWASP API Security
documentations fournisseurs cloud IA
```

Cette veille a permis de justifier le choix d’une solution locale, légère, explicable et maîtrisée.

## 7. Benchmark des modèles et services IA

Le benchmark est documenté dans :

```text
docs/07_ai_service/24_benchmark_modeles_services_ia.md
```

Deux niveaux de comparaison ont été réalisés :

```text
benchmark de modèles internes
benchmark de services IA existants
```

Modèles internes comparés :

```text
business_rules_baseline
dummy_most_frequent
tfidf_logistic_regression
tfidf_linear_svm
tfidf_multinomial_nb
tfidf_random_forest
```

Services IA étudiés :

```text
modèle local scikit-learn
Hugging Face local
Hugging Face Inference Providers
OpenAI API
Google Cloud Natural Language / Vertex AI
Azure AI Language / Azure OpenAI
AWS Comprehend
```

Critères de comparaison :

```text
adéquation fonctionnelle
simplicité
coût
prérequis techniques
confidentialité
dépendance externe
intégration API
maintenance
monitoring
éco-responsabilité
```

## 8. Solution IA retenue

La solution retenue pour la première version est :

```text
TF-IDF + Logistic Regression
```

Justification :

```text
modèle local
faible coût
pas de dépendance cloud obligatoire
pas d’envoi de données à un service externe
rapide à entraîner
explicable en soutenance
facile à intégrer dans FastAPI
compatible avec des tests automatisés
adapté à une preuve de concept pédagogique
sobre en ressources
```

Les services cloud et les LLM externes sont écartés pour la première version, mais restent envisageables dans une évolution future.

## 9. Entraînement et évaluation du modèle

Le modèle est entraîné avec :

```text
src/ai/training/train_intent_classifier.py
```

Artefacts générés :

```text
models/intent_classifier/model.joblib
models/intent_classifier/vectorizer.joblib
models/intent_classifier/label_encoder.joblib
models/intent_classifier/model_metadata.json
```

Rapports générés :

```text
data/ai/reports/model_training_report.csv
data/ai/reports/model_evaluation_report.csv
data/ai/reports/classification_report.csv
data/ai/reports/confusion_matrix.csv
```

## 10. Benchmark expérimental

Le benchmark expérimental est exécuté avec :

```text
src/ai/training/benchmark_intent_models.py
```

Rapports générés :

```text
data/ai/reports/model_benchmark_report.csv
data/ai/reports/model_benchmark_classification_report.csv
data/ai/reports/model_benchmark_selection_report.csv
```

Résultat retenu :

```text
selected_model_name = tfidf_logistic_regression
validation_accuracy = 0.8
validation_macro_f1 = 0.6667
validation_weighted_f1 = 0.7333
```

Ce résultat confirme le choix de la régression logistique avec TF-IDF pour la première version du service IA.

## 11. Module d’inférence

Le module d’inférence est situé dans :

```text
src/ai/inference/intent_predictor.py
```

Il permet de :

```text
charger les artefacts du modèle
prédire l’intention d’un commentaire
prédire un lot de commentaires
retourner un score de confiance
retourner le temps de réponse
fournir les informations du modèle
fournir les métriques disponibles
```

Fonctions principales :

```text
predict_intent()
predict_batch()
get_model_info()
get_model_metrics()
```

## 12. API REST IA

Le modèle IA est exposé via l’API FastAPI existante.

Fichiers principaux :

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
GET  /api/v1/ai/monitoring/dashboard
GET  /api/v1/ai/monitoring/alerts
```

Les routes IA sont protégées par :

```text
X-API-Key
```

## 13. Intégration Docker

L’API est intégrée au `docker-compose.yml` du projet.

Service attendu :

```text
paylive_api
```

L’API est disponible sur :

```text
http://127.0.0.1:8000
```

Documentation Swagger :

```text
http://127.0.0.1:8000/docs
```

## 14. Tests automatisés

Les tests IA sont organisés dans :

```text
tests/test_ai_dataset.py
tests/test_intent_model.py
tests/test_ai_api.py
```

Ils vérifient :

```text
la structure du dataset IA
la présence des classes d’intention
la présence des fichiers train, validation et test
le chargement du modèle
la cohérence des prédictions
les routes API IA
la protection par clé API
les réponses JSON attendues
```

Commande de test :

```bash
pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py -v
```

Rapports générés :

```text
data/ai/reports/ai_dataset_test_report.csv
data/ai/reports/intent_model_test_report.csv
data/ai/reports/ai_api_test_report.csv
```

## 15. Monitoring du modèle IA

Le monitoring est assuré par :

```text
src/ai/monitoring/monitor_predictions.py
```

Fichiers générés :

```text
data/ai/predictions/ai_predictions_log.csv
data/ai/reports/model_monitoring_report.csv
```

Le monitoring suit notamment :

```text
nombre total de prédictions
répartition des intentions prédites
score moyen de confiance
nombre de prédictions à faible confiance
temps moyen de réponse
version du modèle utilisée
source des appels
```

## 16. Dashboard et alertes

Un dashboard HTML de monitoring a été ajouté.

Script :

```text
src/ai/monitoring/generate_monitoring_dashboard.py
```

Fichiers générés :

```text
data/ai/reports/model_monitoring_dashboard.html
data/ai/reports/model_monitoring_alerts.csv
```

Le dashboard affiche :

```text
état global du service IA
nombre total de prédictions
score moyen de confiance
taux de faible confiance
alertes générées
répartition des intentions
répartition par source
répartition par version de modèle
dernières prédictions journalisées
```

Alertes mises en place :

```text
LOW_CONFIDENCE
SLOW_RESPONSE
UNKNOWN_INTENT
```

## 17. Pipeline MLOps et livraison continue

Une chaîne de livraison continue a été créée avec GitHub Actions.

Workflow :

```text
.github/workflows/ai_mlops_ci.yml
```

Le pipeline s’exécute sur :

```text
push
pull_request
workflow_dispatch
```

Il lance automatiquement :

```text
préparation du dataset IA
entraînement du modèle
benchmark des modèles
génération du monitoring
génération du dashboard et des alertes
tests automatisés IA/API
publication des rapports en artefacts GitHub Actions
```

Le pipeline est passé en vert sur GitHub Actions, ce qui valide la logique MLOps légère du projet.

## 18. Couverture des compétences du Bloc 2

| Compétence | Statut | Preuve projet |
|---|---|---|
| Organiser une veille technique et réglementaire liée à l’IA | Validée | `23_veille_technique_reglementaire_ia.md` |
| Définir une thématique de veille | Validée | NLP, IA, API, sécurité, RGPD, AI Act, monitoring |
| Identifier des sources fiables | Validée | sources officielles et réglementaires |
| Produire des synthèses de veille utiles | Validée | synthèse et journal de veille |
| Reformuler le besoin IA du commanditaire | Validée | cadrage et spécifications Bloc 2 |
| Réaliser un benchmark de services IA existants | Validée | benchmark modèles et services IA |
| Comparer fonctionnalités, contraintes, coûts, limites, prérequis, éco-responsabilité | Validée | analyse comparative complète |
| Justifier les services retenus et écartés | Validée | modèle local retenu, services externes écartés |
| Installer et configurer le service IA sélectionné | Validée | modèle entraîné et artefacts sauvegardés |
| Gérer les accès et l’authentification | Validée en POC | routes IA protégées par `X-API-Key` |
| Configurer le monitoring | Validée | logs, rapport, dashboard, alertes |
| Développer une API REST exposant un modèle IA | Validée | routes FastAPI IA |
| Intégrer cette API dans une application | Validée | intégration dans l’API Docker du projet |
| Ajouter authentification, appel API, traitement et affichage | Validée | API key, réponses JSON, Swagger, dashboard |
| Mettre en place des tests d’intégration | Validée | `tests/test_ai_api.py` |
| Monitorer le modèle IA | Validée | métriques de prédiction et santé du service |
| Mettre en place métriques, dashboards et alertes | Validée | dashboard HTML et alertes CSV |
| Programmer des tests automatisés | Validée | tests dataset, modèle et API |
| Créer une chaîne de livraison continue MLOps | Validée | GitHub Actions en vert |

## 19. Limites du Bloc 2

Limites identifiées :

```text
dataset simulé et non issu de commentaires PayLive réels
taille du dataset limitée
score de confiance parfois faible
pas de modèle transformer dans la première version
pas de dashboard temps réel
pas de rôles utilisateurs avancés
pas de réentraînement automatique déclenché en production
pas de déploiement cloud
pas de mesure de drift avancée
```

Ces limites sont acceptées car le projet est une preuve de concept pédagogique locale.

## 20. Évolutions possibles

Évolutions envisageables :

```text
enrichir le dataset avec davantage de formulations
ajouter des fautes d’orthographe simulées
intégrer un modèle transformer local
ajouter l’extraction produit / taille / couleur / quantité
ajouter un retour utilisateur pour corriger les prédictions
mettre en place un réentraînement périodique
ajouter un dashboard plus interactif
connecter le service à une interface vendeur
mettre en place une authentification JWT
déployer l’API sur un cloud
```

## 21. Commandes de vérification finale Bloc 2

Commande complète locale :

```bash
python src/ai/data_preparation/prepare_nlp_dataset.py
python src/ai/training/train_intent_classifier.py
python src/ai/training/benchmark_intent_models.py
python src/ai/monitoring/monitor_predictions.py
python src/ai/monitoring/generate_monitoring_dashboard.py
pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py -v
```

Test API Docker :

```cmd
docker compose up -d
curl -H "X-API-Key: paylive-dev-api-key" -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/api/v1/ai/predict-intent -d "{\"comment_text\":\"je prends la robe noire en M\"}"
```

Téléchargement du dashboard :

```cmd
curl -H "X-API-Key: paylive-dev-api-key" -o dashboard.html http://127.0.0.1:8000/api/v1/ai/monitoring/dashboard
```

## 22. Conclusion

Le Bloc 2 est finalisé.

Le projet dispose désormais d’un service IA complet, local, explicable, testé et monitoré.

Le modèle `TF-IDF + Logistic Regression` répond au besoin principal de classification des commentaires de live shopping, tout en respectant les contraintes de coût, de confidentialité, de simplicité, de reproductibilité et de sobriété.

L’intégration dans FastAPI, la sécurisation par clé API, le dashboard de monitoring, les alertes CSV et le pipeline GitHub Actions permettent de démontrer une démarche professionnelle et cohérente avec une logique MLOps légère.

Le Bloc 2 complète le Bloc 1 en transformant le socle de données en service IA exploitable.
