# Cadrage application Bloc 3 — PayLive AI Copilot

## 1. Objectif du document

Ce document présente le cadrage du **Bloc 3** du projet **PayLive AI Copilot**.

Le Bloc 3 a pour objectif de réaliser une application web intégrant le service d’intelligence artificielle développé dans le Bloc 2.

L’application permettra à un vendeur en live shopping de saisir ou simuler des commentaires de live, d’appeler l’API IA, puis d’afficher clairement l’intention prédite, le score de confiance et les informations utiles pour l’aide à la décision.

L’interface retenue est une application **HTML + CSS + JavaScript**, servie dans un conteneur Docker léger.

## 2. Rappel du contexte projet

**PayLive AI Copilot** est un assistant intelligent destiné aux vendeurs qui réalisent des ventes en direct sur des plateformes comme TikTok Live ou Instagram Live.

Le projet est construit progressivement :

| Bloc | Réalisation principale |
|---|---|
| Bloc 1 | Collecte, nettoyage, stockage PostgreSQL et exposition des données via API REST |
| Bloc 2 | Intégration d’un modèle IA de classification d’intention, API IA, tests, monitoring, dashboard et CI MLOps |
| Bloc 3 | Développement d’une application web consommant l’API IA |

Le Bloc 3 s’appuie donc sur les livrables déjà réalisés :

```text
dataset final IA
base PostgreSQL
API FastAPI
modèle TF-IDF + Logistic Regression
routes IA sécurisées
monitoring IA
dashboard IA
alertes IA
pipeline CI MLOps
```

## 3. Problématique métier

Pendant un live shopping, un vendeur reçoit beaucoup de commentaires en temps réel.

Exemples :

```text
je prends la robe noire en M
combien coûte ce pull ?
vous livrez en Belgique ?
le lien de paiement ne fonctionne pas
```

Le vendeur doit rapidement distinguer :

- les intentions d’achat ;
- les questions produit ;
- les questions paiement ;
- les questions livraison ;
- les messages sans intérêt commercial immédiat ;
- les messages non interprétables.

Le besoin métier est donc de fournir une interface simple qui permet de tester le service IA et de rendre le résultat compréhensible pour un utilisateur non technique.

## 4. Objectifs du Bloc 3

Les objectifs principaux du Bloc 3 sont :

| Objectif | Description |
|---|---|
| Intégrer l’API IA | Consommer les routes IA développées dans FastAPI |
| Créer une interface utilisateur | Fournir une page web claire pour saisir un commentaire |
| Afficher les prédictions | Montrer l’intention prédite et le score de confiance |
| Gérer l’authentification | Envoyer la clé `X-API-Key` lors des appels API |
| Traiter les erreurs | Afficher les erreurs API, réseau ou validation |
| Visualiser le monitoring | Donner accès au dashboard et aux alertes IA |
| Respecter l’accessibilité | Concevoir une interface utilisable au clavier et lisible |
| Conteneuriser l’application | Servir le front HTML/JS dans Docker |
| Tester l’application | Prévoir des tests manuels, fonctionnels et d’intégration |

## 5. Périmètre fonctionnel retenu

Le périmètre de la première version est volontairement simple.

Fonctionnalités incluses :

```text
saisie d’un commentaire
configuration de la clé API
appel de l’API de prédiction d’intention
affichage du résultat IA
affichage du score de confiance
affichage d’un indicateur faible confiance
appel du mode batch sur plusieurs commentaires
consultation des informations du modèle
consultation des métriques du modèle
accès au dashboard de monitoring IA
accès aux alertes IA
interface responsive simple
conteneurisation Docker
```

Fonctionnalités exclues de la première version :

```text
authentification utilisateur complète
création de comptes vendeurs
connexion directe à TikTok ou Instagram
analyse temps réel de vrais lives
paiement réel
stock réel
édition des commandes
back-office complet
framework front complexe type React ou Vue
```

## 6. Choix d’interface

Le choix retenu est :

```text
HTML + CSS + JavaScript natif
```

Ce choix est justifié par :

- la simplicité de développement ;
- la rapidité de mise en œuvre ;
- l’absence de dépendance front lourde ;
- la facilité de démonstration en soutenance ;
- la compatibilité avec Docker et Nginx ;
- la cohérence avec une preuve de concept locale ;
- la possibilité de montrer clairement les appels API.

Le front sera servi via un conteneur Docker dédié, basé sur Nginx.

## 7. Architecture cible simplifiée

```text
Navigateur utilisateur
        ↓
Frontend HTML/CSS/JS — Docker / Nginx
        ↓ appels HTTP avec X-API-Key
API FastAPI — Docker
        ↓
Service IA local
        ↓
Modèle TF-IDF + Logistic Regression
        ↓
Logs, monitoring, dashboard et alertes
```

## 8. Acteurs du projet

| Acteur | Rôle |
|---|---|
| Vendeur live | Utilise l’interface pour analyser un commentaire |
| Responsable commercial | Consulte les signaux d’achat et la qualité des prédictions |
| Développeur IA | Maintient l’API, le modèle et le monitoring |
| Évaluateur / jury | Vérifie la démonstration applicative et l’intégration IA |

## 9. Contraintes techniques

| Contrainte | Décision |
|---|---|
| Application légère | HTML/CSS/JS sans framework lourd |
| Déploiement local | Docker Compose |
| API existante | FastAPI exposée sur le port `8000` |
| Frontend | Nginx exposé sur le port `8080` |
| Authentification | Header `X-API-Key` |
| Données | Données simulées uniquement |
| Monitoring | Dashboard et alertes du Bloc 2 réutilisés |
| Accessibilité | HTML sémantique, labels, navigation clavier, contraste |

## 10. Contraintes RGPD et sécurité

Le projet reste basé sur des données fictives et simulées.

Mesures retenues :

- aucune donnée réelle PayLive ;
- aucun identifiant bancaire réel ;
- aucune connexion à un live réel ;
- commentaires de démonstration fictifs ;
- clé API nécessaire pour appeler les routes protégées ;
- affichage limité des informations retournées ;
- absence de stockage durable côté navigateur pour les données sensibles.

La clé API pourra être saisie dans l’interface et conservée uniquement en mémoire de session pendant la démonstration.

## 11. Critères de réussite du Bloc 3

Le Bloc 3 sera considéré comme réussi si :

| Critère | Validation attendue |
|---|---|
| Application disponible | Le front est accessible sur `http://localhost:8080` |
| API appelée correctement | Le front appelle `POST /api/v1/ai/predict-intent` |
| Authentification fonctionnelle | Le header `X-API-Key` est envoyé |
| Résultat IA affiché | L’intention, la confiance et le statut sont visibles |
| Erreurs gérées | Les erreurs 401, 403, 422, 500 ou réseau sont affichées |
| Monitoring accessible | Le dashboard et les alertes IA sont consultables |
| Accessibilité prise en compte | Labels, navigation clavier et messages lisibles |
| Docker fonctionnel | L’application démarre avec Docker Compose |
| Tests réalisés | Tests manuels et d’intégration documentés |

## 12. Livrables prévus

Livrables applicatifs :

```text
frontend/Dockerfile
frontend/nginx.conf
frontend/public/index.html
frontend/public/assets/css/styles.css
frontend/public/assets/js/config.js
frontend/public/assets/js/app.js
```

Livrables Docker :

```text
docker-compose.yml mis à jour avec le service frontend
```

Livrables de documentation :

```text
docs/08_application/31_cadrage_application_bloc3.md
docs/08_application/32_specifications_fonctionnelles.md
docs/08_application/33_architecture_application.md
docs/08_application/34_user_stories_accessibilite.md
docs/08_application/35_developpement_interface.md
docs/08_application/36_tests_application.md
docs/08_application/37_bilan_bloc3.md
```

Livrables de preuves :

```text
captures d’écran de l’interface
captures d’écran des appels API réussis
captures d’écran Docker Compose
captures d’écran Swagger
rapports de tests
preuve GitHub Actions si intégrée
```

## 13. Décision de cadrage

La solution retenue pour le Bloc 3 est une application web simple, conteneurisée, consommant l’API IA existante.

Cette approche est cohérente avec le projet car elle permet de :

- démontrer concrètement l’usage du modèle IA ;
- présenter une interface compréhensible par un utilisateur métier ;
- conserver une architecture locale maîtrisée ;
- limiter les dépendances ;
- respecter les contraintes de soutenance ;
- couvrir les besoins d’intégration applicative du Bloc 3.
