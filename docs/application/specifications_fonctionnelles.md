# Spécifications fonctionnelles — Application Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document décrit les spécifications fonctionnelles de l’application web du Bloc 3.

L’application doit permettre à un utilisateur de tester le service IA de PayLive AI Copilot depuis une interface web simple, accessible et conteneurisée.

## 2. Utilisateurs cibles

| Utilisateur | Besoin principal |
|---|---|
| Vendeur live | Comprendre rapidement l’intention d’un commentaire |
| Responsable commercial | Visualiser la qualité des prédictions et repérer les signaux d’achat |
| Développeur IA | Tester l’API IA depuis une interface front |
| Jury / évaluateur | Constater l’intégration applicative du service IA |

## 3. Parcours utilisateur principal

### Parcours : prédire l’intention d’un commentaire

```text
1. L’utilisateur ouvre l’application web.
2. Il renseigne ou vérifie la clé API.
3. Il saisit un commentaire de live shopping.
4. Il clique sur le bouton d’analyse.
5. L’application appelle l’API IA.
6. L’application affiche l’intention prédite.
7. L’application affiche le score de confiance.
8. Si la confiance est faible, un message d’alerte est affiché.
```

## 4. Fonctionnalités attendues

## 4.1. Configuration de la clé API

### Description

L’utilisateur doit pouvoir renseigner la clé API utilisée pour appeler les routes protégées.

### Règles fonctionnelles

- La clé API est envoyée dans le header `X-API-Key`.
- La clé API ne doit pas être écrite en dur dans le HTML.
- En développement, une valeur de démonstration peut être préremplie.
- L’utilisateur peut modifier la clé API depuis l’interface.
- Si la clé est absente, l’application affiche un message clair.

### Critères de validation

| Cas | Résultat attendu |
|---|---|
| Clé absente | Message demandant de renseigner la clé API |
| Clé invalide | Message d’erreur 403 lisible |
| Clé valide | L’appel API est autorisé |

## 4.2. Analyse d’un commentaire unique

### Description

L’utilisateur peut saisir un commentaire et lancer une prédiction d’intention.

### Route API utilisée

```text
POST /api/v1/ai/predict-intent
```

### Payload attendu

```json
{
  "comment_text": "je prends la robe noire en M"
}
```

### Résultat attendu

L’interface affiche :

```text
commentaire analysé
intention prédite
score de confiance
statut faible confiance
version du modèle
temps de réponse
```

### Critères de validation

| Cas | Résultat attendu |
|---|---|
| Commentaire valide | La prédiction est affichée |
| Commentaire vide | Message de validation côté interface |
| API indisponible | Message d’erreur réseau |
| Réponse API invalide | Message d’erreur technique lisible |

## 4.3. Analyse de plusieurs commentaires

### Description

L’utilisateur peut saisir plusieurs commentaires, un par ligne, puis lancer une analyse batch.

### Route API utilisée

```text
POST /api/v1/ai/batch-predict-intents
```

### Payload attendu

```json
{
  "comments": [
    "je prends le pull rouge",
    "combien coûte la robe ?",
    "vous livrez en Belgique ?"
  ]
}
```

### Résultat attendu

L’interface affiche un tableau avec :

```text
commentaire
intention prédite
score de confiance
statut faible confiance
temps de réponse
```

### Critères de validation

| Cas | Résultat attendu |
|---|---|
| Plusieurs lignes valides | Un résultat par commentaire |
| Lignes vides | Elles sont ignorées ou signalées |
| Lot vide | Message de validation |
| Erreur API | Message d’erreur global |

## 4.4. Consultation des informations du modèle

### Description

L’utilisateur peut consulter les informations principales du modèle IA utilisé.

### Route API utilisée

```text
GET /api/v1/ai/model-info
```

### Informations affichées

```text
nom du modèle
version
classes disponibles
chemin des artefacts
nombre de classes
date d’entraînement si disponible
```

### Critères de validation

| Cas | Résultat attendu |
|---|---|
| API disponible | Les informations du modèle sont affichées |
| API protégée sans clé | Message d’erreur d’authentification |
| API indisponible | Message d’erreur réseau |

## 4.5. Consultation des métriques du modèle

### Description

L’utilisateur peut consulter les métriques d’évaluation du modèle.

### Route API utilisée

```text
GET /api/v1/ai/model-metrics
```

### Informations affichées

```text
accuracy
macro F1
weighted F1
rapport d’évaluation
résultat du benchmark
```

### Critères de validation

| Cas | Résultat attendu |
|---|---|
| Métriques disponibles | Les métriques sont affichées |
| Métriques absentes | Message indiquant l’absence de rapport |
| Erreur API | Message lisible |

## 4.6. Accès au dashboard de monitoring IA

### Description

L’utilisateur peut accéder au dashboard HTML de monitoring IA généré dans le Bloc 2.

### Route API utilisée

```text
GET /api/v1/ai/monitoring/dashboard
```

### Comportement attendu

L’application peut :

- ouvrir le dashboard dans un nouvel onglet ;
- ou récupérer le HTML via `fetch` avec le header `X-API-Key` ;
- ou proposer un bouton de téléchargement.

### Critères de validation

| Cas | Résultat attendu |
|---|---|
| Clé valide | Le dashboard est accessible |
| Clé absente | Message d’authentification |
| Dashboard non généré | Message de ressource introuvable |

## 4.7. Accès aux alertes IA

### Description

L’utilisateur peut consulter ou télécharger le fichier CSV des alertes IA.

### Route API utilisée

```text
GET /api/v1/ai/monitoring/alerts
```

### Informations attendues

```text
type d’alerte
niveau d’alerte
commentaire concerné
intention prédite
score de confiance
temps de réponse
message d’alerte
```

### Critères de validation

| Cas | Résultat attendu |
|---|---|
| Alertes disponibles | Le fichier CSV est téléchargé ou affiché |
| Aucune alerte | Tableau vide ou message explicite |
| API indisponible | Message d’erreur |

## 5. Règles d’affichage des résultats IA

| Élément | Règle d’affichage |
|---|---|
| `purchase_intent` | Badge “Intention d’achat” |
| `product_question` | Badge “Question produit” |
| `payment_question` | Badge “Question paiement” |
| `shipping_question` | Badge “Question livraison” |
| `other` | Badge “Autre message” |
| `unknown` | Badge “Intention inconnue” |
| Confiance < 0.60 | Alerte “Prédiction à faible confiance” |
| Erreur API | Message dans une zone d’erreur visible |

## 6. Exigences non fonctionnelles

| Exigence | Description |
|---|---|
| Simplicité | Interface simple et directe |
| Accessibilité | Labels, contraste, navigation clavier, messages lisibles |
| Performance | Appels rapides, pas de framework lourd |
| Sécurité | Clé API non versionnée dans le code |
| Maintenabilité | Code organisé en HTML, CSS et JS séparés |
| Docker | Application servie par un conteneur Nginx |
| Compatibilité | Fonctionnement sur navigateur moderne |

## 7. Messages utilisateur prévus

| Situation | Message affiché |
|---|---|
| API OK | “Analyse terminée avec succès.” |
| Clé absente | “Veuillez renseigner une clé API.” |
| Clé invalide | “Clé API invalide ou non autorisée.” |
| Commentaire vide | “Veuillez saisir un commentaire à analyser.” |
| API indisponible | “Impossible de joindre l’API. Vérifiez Docker et le backend.” |
| Faible confiance | “Le modèle est peu sûr de cette prédiction.” |

## 8. Critères d’acceptation globaux

L’application est acceptée si :

- elle est accessible via Docker ;
- l’utilisateur peut saisir un commentaire ;
- l’appel API fonctionne avec `X-API-Key` ;
- le résultat IA est affiché clairement ;
- les erreurs sont compréhensibles ;
- les métriques et le dashboard IA sont accessibles ;
- les exigences d’accessibilité de base sont prises en compte ;
- les tests manuels et d’intégration sont documentés.
