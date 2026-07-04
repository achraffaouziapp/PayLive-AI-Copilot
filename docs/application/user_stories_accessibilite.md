# User stories et accessibilité — Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document présente les user stories de l’application web du Bloc 3 et les objectifs d’accessibilité associés.

L’objectif est de relier chaque besoin utilisateur à des critères d’acceptation vérifiables, en intégrant l’accessibilité dès la conception.

## 2. Personas

## 2.1. Persona 1 — Vendeur live

| Élément | Description |
|---|---|
| Nom | Vendeur live |
| Objectif | Identifier rapidement les commentaires importants |
| Contexte | Anime un live shopping avec beaucoup de commentaires |
| Besoin | Savoir si un commentaire correspond à une intention d’achat |
| Difficulté | Peu de temps pour lire tous les commentaires |

## 2.2. Persona 2 — Responsable commercial

| Élément | Description |
|---|---|
| Nom | Responsable commercial |
| Objectif | Comprendre la qualité des prédictions IA |
| Contexte | Suit la performance des lives |
| Besoin | Consulter les métriques, alertes et résultats du modèle |
| Difficulté | Comprendre les limites du modèle IA |

## 2.3. Persona 3 — Développeur IA

| Élément | Description |
|---|---|
| Nom | Développeur IA |
| Objectif | Tester l’intégration du service IA |
| Contexte | Vérifie API, logs, monitoring et front |
| Besoin | Observer les appels API et les réponses |
| Difficulté | Identifier rapidement les erreurs d’intégration |

## 3. User stories fonctionnelles

## US-01 — Configurer la clé API

**En tant que** utilisateur de l’application,  
**je veux** renseigner une clé API,  
**afin de** pouvoir appeler les routes IA protégées.

### Critères d’acceptation

- Un champ permet de saisir la clé API.
- Le champ possède un label visible.
- La clé est envoyée dans le header `X-API-Key`.
- Si la clé est absente, un message explicite est affiché.
- Le champ est accessible au clavier.

### Critères d’accessibilité

- Le champ est associé à un élément `<label>`.
- Le message d’erreur est visible et lisible.
- Le focus clavier est visible.

## US-02 — Analyser un commentaire

**En tant que** vendeur live,  
**je veux** saisir un commentaire,  
**afin de** connaître l’intention prédite par l’IA.

### Critères d’acceptation

- Un champ texte permet de saisir un commentaire.
- Un bouton lance l’analyse.
- L’application appelle `POST /api/v1/ai/predict-intent`.
- Le résultat affiche l’intention prédite.
- Le résultat affiche le score de confiance.
- Le résultat affiche un message si la confiance est faible.

### Critères d’accessibilité

- Le champ commentaire possède un label.
- Le bouton est activable au clavier.
- Le résultat est annoncé dans une zone `aria-live`.
- Le résultat ne dépend pas uniquement d’une couleur.

## US-03 — Comprendre le résultat IA

**En tant que** utilisateur métier,  
**je veux** voir un libellé compréhensible,  
**afin de** comprendre le résultat sans connaître les noms techniques des classes.

### Critères d’acceptation

| Classe technique | Libellé affiché |
|---|---|
| `purchase_intent` | Intention d’achat |
| `product_question` | Question produit |
| `payment_question` | Question paiement |
| `shipping_question` | Question livraison |
| `other` | Autre message |
| `unknown` | Intention inconnue |

### Critères d’accessibilité

- Les libellés sont textuels.
- Les badges sont accompagnés d’un texte explicite.
- Le sens n’est pas porté uniquement par la couleur.

## US-04 — Analyser plusieurs commentaires

**En tant que** vendeur live,  
**je veux** analyser plusieurs commentaires en une seule action,  
**afin de** tester rapidement plusieurs situations.

### Critères d’acceptation

- Une zone de texte permet de saisir plusieurs commentaires.
- Un commentaire est placé par ligne.
- Les lignes vides sont ignorées.
- L’application appelle `POST /api/v1/ai/batch-predict-intents`.
- Les résultats sont affichés dans un tableau.

### Critères d’accessibilité

- Le tableau possède des en-têtes explicites.
- La zone de texte possède une consigne visible.
- Le résultat est lisible au clavier et par lecteur d’écran.

## US-05 — Consulter les informations du modèle

**En tant que** responsable commercial,  
**je veux** consulter les informations du modèle IA,  
**afin de** savoir quel modèle est utilisé.

### Critères d’acceptation

- Un bouton permet de charger les informations du modèle.
- L’application appelle `GET /api/v1/ai/model-info`.
- Les classes disponibles sont affichées.
- La version ou les métadonnées du modèle sont affichées si disponibles.

### Critères d’accessibilité

- Les informations sont structurées avec des titres.
- Les messages de chargement et d’erreur sont lisibles.

## US-06 — Consulter les métriques du modèle

**En tant que** responsable commercial,  
**je veux** consulter les métriques du modèle,  
**afin de** évaluer sa qualité.

### Critères d’acceptation

- Un bouton permet de charger les métriques.
- L’application appelle `GET /api/v1/ai/model-metrics`.
- Les métriques principales sont affichées.
- Les limites du modèle sont rappelées.

### Critères d’accessibilité

- Les métriques ne sont pas uniquement représentées par une couleur.
- Les valeurs numériques sont accompagnées d’un libellé.

## US-07 — Accéder au dashboard IA

**En tant que** développeur IA ou responsable commercial,  
**je veux** accéder au dashboard de monitoring IA,  
**afin de** suivre les prédictions et alertes.

### Critères d’acceptation

- Un bouton permet d’ouvrir ou de charger le dashboard.
- L’application appelle `GET /api/v1/ai/monitoring/dashboard`.
- Si la clé API est valide, le dashboard est accessible.
- En cas d’erreur, un message est affiché.

### Critères d’accessibilité

- Le bouton possède un intitulé clair.
- Le chargement du dashboard est annoncé.
- Le lien ou bouton est utilisable au clavier.

## US-08 — Consulter les alertes IA

**En tant que** développeur IA,  
**je veux** consulter les alertes de monitoring,  
**afin de** identifier les prédictions à faible confiance ou les réponses lentes.

### Critères d’acceptation

- Un bouton permet de télécharger ou afficher les alertes.
- L’application appelle `GET /api/v1/ai/monitoring/alerts`.
- Les alertes sont affichées ou téléchargées.

### Critères d’accessibilité

- Le bouton est accessible au clavier.
- Le format CSV est signalé clairement.
- Une alternative textuelle explique le contenu du fichier.

## US-09 — Gérer les erreurs API

**En tant que** utilisateur,  
**je veux** comprendre les erreurs,  
**afin de** savoir quoi corriger.

### Critères d’acceptation

| Erreur | Message attendu |
|---|---|
| 401 | Clé API manquante |
| 403 | Clé API invalide |
| 422 | Données envoyées invalides |
| 500 | Erreur serveur |
| Erreur réseau | API inaccessible |

### Critères d’accessibilité

- Les erreurs sont affichées dans une zone dédiée.
- Les erreurs sont annoncées avec `aria-live`.
- Les erreurs ne disparaissent pas trop vite.

## US-10 — Utiliser l’application au clavier

**En tant que** utilisateur ayant besoin d’une navigation clavier,  
**je veux** utiliser toute l’application sans souris,  
**afin de** accéder aux fonctionnalités principales.

### Critères d’acceptation

- Tous les champs sont accessibles avec Tab.
- Tous les boutons sont activables avec Entrée ou Espace.
- L’ordre de tabulation est logique.
- Le focus est visible.

### Critères d’accessibilité

- Aucun élément interactif n’est inaccessible au clavier.
- Les zones dynamiques sont annoncées.

## 4. Objectifs techniques d’accessibilité

Les objectifs d’accessibilité retenus sont :

| Objectif | Mise en œuvre prévue |
|---|---|
| HTML sémantique | Utiliser `header`, `main`, `section`, `footer` |
| Labels explicites | Associer chaque champ à un `<label>` |
| Navigation clavier | Utiliser des boutons natifs et liens natifs |
| Focus visible | Style CSS de focus clair |
| Contraste suffisant | Couleurs sobres et lisibles |
| Messages dynamiques | Zones `aria-live` pour résultats et erreurs |
| Langue de page | Attribut `lang="fr"` |
| Tableaux lisibles | En-têtes `<th>` et structure correcte |
| Responsive | Interface utilisable sur écran réduit |
| Pas de couleur seule | Ajouter texte et icônes textuelles |

## 5. Wireframe textuel

```text
+--------------------------------------------------+
| PayLive AI Copilot — Interface vendeur           |
+--------------------------------------------------+
| Configuration                                    |
| [ Clé API _________________________ ]            |
+--------------------------------------------------+
| Analyse d’un commentaire                         |
| [ Commentaire à analyser __________________ ]    |
| [ Analyser le commentaire ]                      |
|                                                  |
| Résultat IA                                      |
| Intention : Intention d’achat                    |
| Confiance : 0.82                                 |
| Statut : OK                                      |
+--------------------------------------------------+
| Analyse batch                                    |
| [ Zone plusieurs commentaires ]                  |
| [ Analyser le lot ]                              |
| [ Tableau de résultats ]                         |
+--------------------------------------------------+
| Modèle et monitoring                             |
| [ Infos modèle ] [ Métriques ]                   |
| [ Dashboard ] [ Alertes ]                        |
+--------------------------------------------------+
```

## 6. Grille de validation accessibilité

| Contrôle | Statut attendu |
|---|---|
| Page avec `lang="fr"` | OK |
| Champs avec labels | OK |
| Boutons natifs | OK |
| Navigation clavier complète | OK |
| Focus visible | OK |
| Messages d’erreur visibles | OK |
| Résultats annoncés | OK |
| Tableaux structurés | OK |
| Contrastes lisibles | OK |
| Interface responsive | OK |

## 7. Conclusion

Les user stories définissent un périmètre clair pour l’application du Bloc 3.

Les critères d’accessibilité sont intégrés directement dans les critères d’acceptation, ce qui permet de vérifier l’utilisabilité de l’interface pendant le développement et les tests.
