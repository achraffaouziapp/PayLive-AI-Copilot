# Veille technique et réglementaire IA — PayLive AI Copilot

## 1. Objectif du document

Ce document présente la veille technique et réglementaire réalisée dans le cadre du Bloc 2 du projet **PayLive AI Copilot**.

Le Bloc 2 vise à intégrer un service d’intelligence artificielle capable d’analyser des commentaires de live shopping et de prédire l’intention exprimée par l’utilisateur.

La veille permet de justifier les choix techniques et de prendre en compte les contraintes liées à l’IA, aux API, à la sécurité, au RGPD et au cadre réglementaire européen.

## 2. Périmètre de la veille

La veille porte sur les thématiques suivantes :

| Thématique | Objectif |
|---|---|
| NLP et classification de texte | Identifier les approches adaptées à l’analyse de commentaires courts |
| Machine learning supervisé | Choisir un modèle adapté aux données du projet |
| API IA | Exposer le modèle via une API REST documentée |
| Sécurité API | Protéger les routes IA et limiter les accès non autorisés |
| Monitoring IA | Suivre les prédictions et la qualité du modèle |
| RGPD | Limiter les risques liés aux données personnelles |
| AI Act | Prendre en compte le cadre réglementaire européen sur l’IA |
| MLOps léger | Organiser les artefacts, les rapports, les tests et le suivi du modèle |

## 3. Organisation de la veille

La veille est organisée autour de trois axes :

```text
veille technique
veille réglementaire
veille sécurité / qualité
```

La veille technique concerne les outils, bibliothèques et architectures permettant d’intégrer un service IA.

La veille réglementaire concerne les obligations ou bonnes pratiques liées à l’utilisation de données et de systèmes d’intelligence artificielle.

La veille sécurité / qualité concerne la sécurisation de l’API, la documentation, les tests et le monitoring.

## 4. Sources principales utilisées

| Source | Type | Utilisation dans le projet |
|---|---|---|
| Documentation scikit-learn | technique | Vectorisation TF-IDF, modèles de classification, métriques |
| Documentation FastAPI | technique | Création de routes API, sécurité par API key, OpenAPI |
| OpenAPI Initiative | technique | Standard de documentation des API REST |
| CNIL | réglementaire | Recommandations IA et RGPD |
| EUR-Lex | réglementaire | Texte officiel du règlement européen sur l’IA |
| OWASP API Security | sécurité | Bonnes pratiques de sécurisation des API |
| Documentation Python / joblib | technique | Sauvegarde et chargement des artefacts du modèle |

## 5. Critères de sélection des sources

Les sources sont sélectionnées selon les critères suivants :

- source officielle ou institutionnelle ;
- documentation maintenue ;
- date récente ou contenu stable ;
- lien direct avec le projet ;
- utilité pour justifier un choix technique ;
- possibilité de retrouver l’information facilement ;
- crédibilité de l’organisme éditeur.

## 6. Veille technique — NLP et classification de texte

Le besoin du projet est de classifier des commentaires courts issus de lives shopping.

Exemples :

```text
je prends le pull rouge
combien coûte cette robe ?
vous livrez en Belgique ?
le lien de paiement marche ?
```

Le problème correspond à une classification supervisée de texte.

Approches identifiées :

| Approche | Description |
|---|---|
| Règles simples | Détection par mots-clés |
| TF-IDF + modèle linéaire | Transformation des textes en vecteurs puis classification |
| SVM linéaire | Modèle souvent performant sur texte court |
| Random Forest | Modèle de comparaison non linéaire |
| Transformer local | Modèle NLP avancé basé sur des représentations contextuelles |
| LLM externe | Service IA tiers appelé via API |

## 7. Veille technique — TF-IDF

TF-IDF signifie **Term Frequency - Inverse Document Frequency**.

Cette méthode transforme un texte en vecteur numérique en tenant compte :

- de la fréquence d’un mot dans un document ;
- de la rareté de ce mot dans l’ensemble du corpus.

Dans le projet, TF-IDF est adapté car :

- les commentaires sont courts ;
- le dataset reste de taille limitée ;
- l’approche est rapide ;
- le résultat est facilement exploitable par scikit-learn ;
- la méthode est explicable en soutenance.

Exemple :

```text
"je prends le pull rouge"
```

Le texte est transformé en variables numériques représentant les mots ou groupes de mots présents.

## 8. Veille technique — Logistic Regression

La régression logistique est un modèle de classification supervisée.

Dans le projet, elle est utilisée pour prédire une classe d’intention parmi :

```text
purchase_intent
product_question
payment_question
shipping_question
other
unknown
```

Avantages pour le projet :

- rapide à entraîner ;
- adaptée à une première version ;
- compatible avec les matrices TF-IDF ;
- permet d’obtenir des probabilités ;
- simple à sauvegarder et à charger ;
- facile à intégrer dans une API.

Limites :

- ne comprend pas réellement le contexte ;
- sensible à la qualité du dataset ;
- moins performante qu’un modèle transformer sur des phrases très ambiguës.

## 9. Veille technique — Modèles avancés

Des modèles plus avancés peuvent être envisagés plus tard :

```text
CamemBERT
DistilBERT
Sentence Transformers
LLM externe
```

Avantages :

- meilleure compréhension du contexte ;
- meilleure robustesse aux formulations variées ;
- meilleure gestion des textes ambigus.

Limites :

- dépendances plus lourdes ;
- temps d’entraînement supérieur ;
- besoin de plus de ressources ;
- complexité plus élevée ;
- justification plus difficile pour une première version locale.

Décision :

```text
ne pas utiliser de modèle avancé dans la première version du Bloc 2
```

Ces modèles sont conservés comme évolutions possibles.

## 10. Veille technique — API IA avec FastAPI

Le projet utilise déjà FastAPI pour exposer les données du Bloc 1.

Le service IA sera intégré à cette API existante afin de conserver une architecture cohérente.

Routes prévues :

```text
POST /api/v1/ai/predict-intent
POST /api/v1/ai/batch-predict-intents
GET  /api/v1/ai/model-info
GET  /api/v1/ai/model-metrics
```

FastAPI est adapté au projet car :

- il est déjà intégré ;
- il permet une documentation Swagger automatique ;
- il supporte les modèles Pydantic ;
- il permet de protéger des routes ;
- il est simple à tester avec Pytest et TestClient.

## 11. Veille technique — OpenAPI

OpenAPI permet de décrire une API HTTP de manière standardisée.

Dans le projet, OpenAPI est utilisé via FastAPI pour :

- documenter les routes IA ;
- décrire les schémas d’entrée ;
- décrire les schémas de sortie ;
- tester les routes depuis Swagger ;
- faciliter la compréhension du service IA.

La documentation sera accessible localement :

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/openapi.json
```

## 12. Veille sécurité — API key

Les routes IA manipulent des prédictions et doivent être protégées.

Le mécanisme retenu est :

```text
X-API-Key
```

Ce choix est cohérent avec le Bloc 1.

Comportement attendu :

| Cas | Réponse attendue |
|---|---|
| clé API absente | 401 Unauthorized |
| clé API invalide | 403 Forbidden |
| clé API valide | 200 OK |

Cette sécurité reste simple, adaptée à une preuve de concept locale.

Limites :

- pas de gestion multi-utilisateurs ;
- pas d’expiration automatique de clé ;
- pas de rôles avancés ;
- pas de JWT.

Évolution possible :

```text
remplacer X-API-Key par OAuth2 ou JWT dans une version production
```

## 13. Veille sécurité — OWASP API

Les bonnes pratiques OWASP API Security rappellent l’importance de :

- contrôler l’authentification ;
- limiter les accès non autorisés ;
- valider les entrées ;
- éviter l’exposition excessive de données ;
- surveiller les erreurs ;
- documenter les contrôles de sécurité.

Application au projet :

| Risque | Mesure appliquée |
|---|---|
| accès non autorisé aux prédictions | X-API-Key |
| commentaire vide ou invalide | validation Pydantic |
| fuite de données sensibles | données simulées et réponse limitée |
| erreurs non contrôlées | gestion des exceptions |
| manque de traçabilité | logs et rapports de monitoring |

## 14. Veille réglementaire — RGPD

Même si le projet utilise des données simulées, les commentaires de live peuvent, dans un contexte réel, contenir des données personnelles.

Exemples de données possibles :

- pseudonyme ;
- prénom ;
- adresse ;
- demande de livraison ;
- information de commande ;
- information personnelle écrite dans un commentaire.

Mesures retenues dans le projet :

- aucune donnée réelle PayLive ;
- données générées et simulées ;
- identifiants clients pseudonymisés ;
- absence de données bancaires ;
- pas d’adresse réelle ;
- logs limités ;
- documentation dans le registre RGPD ;
- minimisation des données exposées par l’API IA.

## 15. Veille réglementaire — CNIL et IA

La CNIL publie des fiches pratiques et recommandations concernant le développement de systèmes d’IA conformes au RGPD.

Points importants pour le projet :

- documenter le traitement ;
- identifier les données utilisées ;
- limiter les données collectées ;
- sécuriser les accès ;
- conserver une traçabilité ;
- prévoir une analyse des risques ;
- informer sur les limites du modèle ;
- éviter l’utilisation inutile de données personnelles.

Application au projet :

| Recommandation | Application |
|---|---|
| minimisation | seules les colonnes nécessaires au modèle sont utilisées |
| sécurité | API protégée par clé |
| documentation | documents Bloc 2 et registre RGPD |
| traçabilité | rapports et logs de prédiction |
| maîtrise des données | données simulées uniquement |

## 16. Veille réglementaire — AI Act

Le règlement européen sur l’intelligence artificielle introduit un cadre harmonisé pour l’IA dans l’Union européenne.

Dans le cadre du projet, le système IA est :

- local ;
- pédagogique ;
- basé sur des données simulées ;
- utilisé comme aide à la décision ;
- sans décision automatique critique ;
- sans impact juridique sur une personne.

Le projet ne correspond pas à un système IA critique ou à haut risque dans sa forme actuelle.

Mesures retenues :

- documenter le modèle ;
- documenter les données utilisées ;
- garder une traçabilité des prédictions ;
- informer sur les limites ;
- éviter les données réelles ;
- contrôler les accès ;
- monitorer les prédictions.

## 17. Veille MLOps léger

Le projet ne nécessite pas une plateforme MLOps complète.

Un MLOps léger est suffisant pour le Bloc 2.

Éléments retenus :

| Élément | Mise en œuvre |
|---|---|
| version du modèle | model_metadata.json |
| artefacts | models/intent_classifier/ |
| dataset | data/ai/datasets/ |
| rapports | data/ai/reports/ |
| logs de prédiction | data/ai/predictions/ |
| tests | tests/test_ai_*.py |
| monitoring | monitor_predictions.py |

## 18. Veille monitoring IA

Le monitoring du modèle doit suivre :

- nombre total de prédictions ;
- répartition des classes prédites ;
- score moyen de confiance ;
- prédictions à faible confiance ;
- temps moyen de réponse ;
- version du modèle utilisée.

Objectif :

- détecter les comportements anormaux ;
- repérer les prédictions incertaines ;
- préparer une future amélioration du modèle ;
- conserver une preuve de fonctionnement.

## 19. Synthèse des choix issus de la veille

| Sujet | Choix retenu |
|---|---|
| Problème IA | classification de texte supervisée |
| Texte d’entrée | comment_text |
| Cible | manual_intent_label |
| Modèle principal | TF-IDF + Logistic Regression |
| Benchmark | DummyClassifier, règles, Logistic Regression, SVM, Random Forest |
| API | FastAPI |
| Documentation API | Swagger / OpenAPI |
| Sécurité | X-API-Key |
| Monitoring | CSV local + rapports |
| Données | données simulées |
| RGPD | minimisation et pseudonymisation |
| AI Act | documentation, traçabilité, limites du modèle |

## 20. Limites identifiées par la veille

Limites de la première version :

- modèle dépendant des labels simulés ;
- pas de compréhension profonde du contexte ;
- robustesse limitée face aux fautes importantes ;
- pas de modèle transformer dans la première version ;
- pas de service IA externe ;
- pas de monitoring en temps réel ;
- pas de déploiement cloud.

Ces limites sont acceptées car le projet reste une preuve de concept pédagogique locale.

## 21. Évolutions envisagées

Évolutions possibles :

- intégrer un modèle transformer local ;
- ajouter un système de retour utilisateur ;
- améliorer la qualité des labels ;
- ajouter l’extraction produit / taille / couleur / quantité ;
- ajouter un tableau de bord de monitoring ;
- mettre en place un système de réentraînement ;
- ajouter une authentification plus avancée ;
- préparer un déploiement cloud.

## 22. Sources de veille

Sources utilisées :

- scikit-learn — TfidfVectorizer  
  https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

- scikit-learn — LogisticRegression  
  https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

- FastAPI — Security Tools  
  https://fastapi.tiangolo.com/reference/security/

- FastAPI — Security Tutorial  
  https://fastapi.tiangolo.com/tutorial/security/

- OpenAPI Initiative  
  https://www.openapis.org/

- CNIL — Les fiches pratiques IA  
  https://www.cnil.fr/fr/les-fiches-pratiques-ia

- EUR-Lex — Regulation (EU) 2024/1689 Artificial Intelligence Act  
  https://eur-lex.europa.eu/eli/reg/2024/1689/oj

- OWASP API Security Project  
  https://owasp.org/www-project-api-security/

## 23. Conclusion

La veille technique et réglementaire confirme que l’approche retenue est adaptée au projet.

Le choix d’un modèle **TF-IDF + Logistic Regression** permet de construire une première version simple, locale, explicable, testable et intégrable dans FastAPI.

La prise en compte du RGPD, de la sécurité API, du monitoring et du cadre européen de l’IA permet de construire un service IA documenté et maîtrisé.

Cette veille servira de justification aux choix techniques du Bloc 2 et de base pour les évolutions futures du projet.
