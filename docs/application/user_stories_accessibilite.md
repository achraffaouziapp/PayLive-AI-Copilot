# User stories et accessibilité — Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document présente les user stories de l’application web du Bloc 3 et les objectifs d’accessibilité associés.

L’objectif est de relier chaque besoin utilisateur à des critères d’acceptation vérifiables, en intégrant l’accessibilité dès la conception.

## 2. Référentiel d’accessibilité retenu

**Référentiel retenu : WCAG 2.2 niveau AA / RGAA.**

Les objectifs d’accessibilité sont intégrés directement dans les critères d’acceptation des user stories afin d’être vérifiables pendant le développement et les tests.

Les quatre critères transverses utilisés sont :

- **AC-A11Y-01 — Navigation clavier :** la fonctionnalité doit être utilisable entièrement au clavier, avec un ordre de tabulation logique et un focus visible.
- **AC-A11Y-02 — Labels :** tout champ de formulaire présent dans la fonctionnalité doit posséder un label explicite et correctement associé.
- **AC-A11Y-03 — Contraste :** les textes, composants interactifs et informations visuelles doivent respecter les exigences de contraste du **WCAG 2.2 niveau AA**.
- **AC-A11Y-04 — Messages dynamiques :** tout résultat, changement de statut ou message d’erreur affiché dynamiquement doit être annoncé aux technologies d’assistance, notamment avec `aria-live` lorsque cela est pertinent.

Ces critères sont complétés par les principes du RGAA concernant notamment la structure sémantique, les formulaires, la navigation au clavier, les tableaux, les contrastes et les contenus dynamiques.

## 3. Personas

### 3.1. Persona 1 — Vendeur live

| Élément | Description |
|---|---|
| Nom | Vendeur live |
| Objectif | Identifier rapidement les commentaires importants |
| Contexte | Anime un live shopping avec beaucoup de commentaires |
| Besoin | Savoir si un commentaire correspond à une intention d’achat |
| Difficulté | Peu de temps pour lire tous les commentaires |

### 3.2. Persona 2 — Responsable commercial

| Élément | Description |
|---|---|
| Nom | Responsable commercial |
| Objectif | Comprendre la qualité des prédictions IA |
| Contexte | Suit la performance des lives |
| Besoin | Consulter les métriques, alertes et résultats du modèle |
| Difficulté | Comprendre les limites du modèle IA |

### 3.3. Persona 3 — Développeur IA

| Élément | Description |
|---|---|
| Nom | Développeur IA |
| Objectif | Tester l’intégration du service IA |
| Contexte | Vérifie API, logs, monitoring et front |
| Besoin | Observer les appels API et les réponses |
| Difficulté | Identifier rapidement les erreurs d’intégration |

## 4. User stories fonctionnelles

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
- **AC-A11Y-01 :** le champ et les actions associées sont entièrement utilisables au clavier, avec un focus visible.
- **AC-A11Y-02 :** le champ de clé API possède un label explicite et correctement associé.
- **AC-A11Y-03 :** le contraste du champ, du label, du focus et des messages respecte le **WCAG 2.2 niveau AA**.
- **AC-A11Y-04 :** les messages de validation ou d’erreur sont annoncés via une zone dynamique adaptée, notamment `aria-live`.

### Critères d’accessibilité complémentaires

- Le message d’erreur est visible et lisible.
- Le focus clavier est clairement perceptible.

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
- **AC-A11Y-01 :** la saisie et le lancement de l’analyse sont entièrement utilisables au clavier.
- **AC-A11Y-02 :** le champ commentaire possède un label explicite et correctement associé.
- **AC-A11Y-03 :** les textes, boutons, états de focus et messages respectent le **WCAG 2.2 niveau AA**.
- **AC-A11Y-04 :** le résultat de prédiction et les éventuels messages d’erreur sont annoncés avec `aria-live`.

### Critères d’accessibilité complémentaires

- Le résultat ne dépend pas uniquement d’une couleur.
- Le score de confiance reste disponible sous forme textuelle.

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

- **AC-A11Y-01 :** les informations et actions associées au résultat restent accessibles au clavier.
- **AC-A11Y-02 :** tout champ éventuellement associé au résultat possède un label explicite et correctement associé.
- **AC-A11Y-03 :** les libellés, badges et états visuels respectent le contraste **WCAG 2.2 niveau AA**.
- **AC-A11Y-04 :** lorsqu’un résultat est mis à jour dynamiquement, sa nouvelle valeur est annoncée avec `aria-live`.

### Critères d’accessibilité complémentaires

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
- **AC-A11Y-01 :** la zone de saisie, le bouton d’analyse et le tableau de résultat sont navigables au clavier.
- **AC-A11Y-02 :** la zone de texte possède un label explicite et correctement associé.
- **AC-A11Y-03 :** le champ, les boutons, le tableau et les états de focus respectent le **WCAG 2.2 niveau AA**.
- **AC-A11Y-04 :** la disponibilité des résultats du batch ou les erreurs sont annoncées avec `aria-live`.

### Critères d’accessibilité complémentaires

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
- **AC-A11Y-01 :** le bouton et les informations affichées sont accessibles au clavier.
- **AC-A11Y-02 :** tout champ éventuellement présent possède un label explicite et correctement associé.
- **AC-A11Y-03 :** les textes, boutons et états de focus respectent le **WCAG 2.2 niveau AA**.
- **AC-A11Y-04 :** les messages de chargement, de succès ou d’erreur sont annoncés avec `aria-live`.

### Critères d’accessibilité complémentaires

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
- **AC-A11Y-01 :** le chargement et la consultation des métriques sont entièrement utilisables au clavier.
- **AC-A11Y-02 :** tout champ présent dans cette fonctionnalité possède un label correctement associé.
- **AC-A11Y-03 :** les valeurs, libellés et composants respectent le contraste **WCAG 2.2 niveau AA**.
- **AC-A11Y-04 :** le chargement, la mise à jour ou les erreurs liés aux métriques sont annoncés avec `aria-live`.

### Critères d’accessibilité complémentaires

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
- **AC-A11Y-01 :** l’accès au dashboard est entièrement réalisable au clavier.
- **AC-A11Y-02 :** tout champ éventuellement utilisé pour la consultation possède un label correctement associé.
- **AC-A11Y-03 :** les textes, boutons et informations graphiques respectent le **WCAG 2.2 niveau AA**.
- **AC-A11Y-04 :** les messages de chargement, d’ouverture ou d’erreur sont annoncés avec `aria-live`.

### Critères d’accessibilité complémentaires

- Le bouton possède un intitulé clair.
- Les données essentielles du dashboard restent disponibles sous forme textuelle ou tabulaire.

## US-08 — Consulter les alertes IA

**En tant que** développeur IA,  
**je veux** consulter les alertes de monitoring,  
**afin de** identifier les prédictions à faible confiance ou les réponses lentes.

### Critères d’acceptation

- Un bouton permet de télécharger ou afficher les alertes.
- L’application appelle `GET /api/v1/ai/monitoring/alerts`.
- Les alertes sont affichées ou téléchargées.
- **AC-A11Y-01 :** le bouton de consultation ou de téléchargement est entièrement utilisable au clavier.
- **AC-A11Y-02 :** tout champ éventuellement présent possède un label explicite et correctement associé.
- **AC-A11Y-03 :** les alertes, boutons et états visuels respectent le **WCAG 2.2 niveau AA**.
- **AC-A11Y-04 :** le succès, l’échec ou la disponibilité du téléchargement sont annoncés avec `aria-live`.

### Critères d’accessibilité complémentaires

- Le format CSV est signalé clairement.
- Une alternative textuelle explique le contenu du fichier.
- Le niveau d’alerte ne dépend pas uniquement de la couleur.

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

- **AC-A11Y-01 :** l’utilisateur peut atteindre les éléments concernés et poursuivre la navigation entièrement au clavier après une erreur.
- **AC-A11Y-02 :** lorsqu’une erreur concerne un champ, celui-ci conserve un label explicite et correctement associé.
- **AC-A11Y-03 :** les messages d’erreur respectent le contraste **WCAG 2.2 niveau AA** et ne reposent pas uniquement sur la couleur.
- **AC-A11Y-04 :** les erreurs sont annoncées dans une zone `aria-live`.

### Critères d’accessibilité complémentaires

- Les erreurs sont affichées dans une zone dédiée.
- Les erreurs ne disparaissent pas trop vite.
- Le texte indique clairement l’action corrective attendue lorsque celle-ci est connue.

## US-10 — Utiliser l’application au clavier

**En tant que** utilisateur ayant besoin d’une navigation clavier,  
**je veux** utiliser toute l’application sans souris,  
**afin de** accéder aux fonctionnalités principales.

### Critères d’acceptation

- Tous les champs sont accessibles avec Tab.
- Tous les boutons sont activables avec Entrée ou Espace.
- L’ordre de tabulation est logique.
- Le focus est visible.
- **AC-A11Y-01 :** l’ensemble des fonctionnalités principales est utilisable complètement au clavier.
- **AC-A11Y-02 :** chaque champ atteint au clavier possède un label explicite et correctement associé.
- **AC-A11Y-03 :** le focus, les textes et les composants interactifs respectent les exigences de contraste du **WCAG 2.2 niveau AA**.
- **AC-A11Y-04 :** les changements de statut, résultats et erreurs déclenchés au clavier sont annoncés avec `aria-live`.

### Critères d’accessibilité complémentaires

- Aucun élément interactif n’est inaccessible au clavier.
- Les zones dynamiques sont annoncées.
- Aucun piège au clavier ne bloque la navigation.

## 5. Objectifs techniques d’accessibilité

**Référentiel retenu : WCAG 2.2 niveau AA / RGAA.**

Les objectifs d’accessibilité retenus sont :

| Objectif | Mise en œuvre prévue |
|---|---|
| HTML sémantique | Utiliser `header`, `main`, `section`, `footer` |
| Labels explicites | Associer chaque champ à un `<label>` |
| Navigation clavier | Utiliser des boutons natifs et liens natifs |
| Focus visible | Style CSS de focus clair |
| Contraste suffisant | Vérifier les contrastes selon WCAG 2.2 niveau AA |
| Messages dynamiques | Zones `aria-live` pour résultats, statuts et erreurs |
| Langue de page | Attribut `lang="fr"` |
| Tableaux lisibles | En-têtes `<th>` et structure correcte |
| Responsive | Interface utilisable sur écran réduit |
| Pas de couleur seule | Ajouter du texte ou un indicateur explicite en complément |

## 6. Wireframe textuel

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

## 7. Grille de validation accessibilité

| Contrôle | Référence | Statut attendu |
|---|---|---|
| Page avec `lang="fr"` | RGAA / WCAG | OK |
| Champs avec labels correctement associés | AC-A11Y-02 | OK |
| Boutons natifs | RGAA / WCAG | OK |
| Navigation clavier complète | AC-A11Y-01 | OK |
| Focus visible | AC-A11Y-01 | OK |
| Messages d’erreur visibles | RGAA / WCAG | OK |
| Résultats et statuts dynamiques annoncés | AC-A11Y-04 | OK |
| Tableaux structurés | RGAA / WCAG | OK |
| Contrastes conformes WCAG 2.2 niveau AA | AC-A11Y-03 | OK |
| Interface responsive | objectif d’utilisabilité | OK |
| Information non transmise uniquement par couleur | WCAG / RGAA | OK |

## 8. Preuves de validation recommandées

Pour démontrer la prise en compte des critères d’acceptation, les preuves suivantes peuvent être conservées :

```text
preuve_c14_navigation_clavier.png
preuve_c14_focus_visible.png
preuve_c14_labels_formulaire.png
preuve_c14_contraste_wcag_aa.png
preuve_c14_aria_live_resultat.png
preuve_c14_aria_live_erreur.png
```

Il est également possible de conserver :

- une capture du code HTML montrant les associations `<label for="...">` / `id` ;
- une capture du focus clavier sur les principaux boutons ;
- une capture du résultat d’un outil de vérification de contraste ;
- une capture du code contenant `aria-live` sur les zones dynamiques ;
- une capture des tickets Jira contenant les critères d’acceptation d’accessibilité.

## 9. Conclusion

Les user stories définissent un périmètre clair pour l’application et intègrent désormais explicitement les objectifs d’accessibilité dans leurs critères d’acceptation.

Le **référentiel retenu est WCAG 2.2 niveau AA / RGAA**.

Les critères transverses `AC-A11Y-01` à `AC-A11Y-04` permettent de vérifier :

- l’utilisation complète au clavier ;
- l’association correcte des labels aux champs ;
- la conformité des contrastes au niveau AA ;
- l’annonce des messages dynamiques avec `aria-live`.

L’accessibilité peut ainsi être contrôlée au même titre que les autres exigences fonctionnelles pendant le développement, les tests et la validation de l’application.
