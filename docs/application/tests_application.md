# Tests de l’application — Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document décrit la stratégie de test de l’application web du Bloc 3.

Les tests doivent vérifier que l’interface HTML/CSS/JavaScript :

- se lance correctement dans Docker ;
- communique avec l’API FastAPI ;
- envoie la clé API ;
- affiche les résultats IA ;
- gère les erreurs ;
- respecte les critères d’accessibilité de base.

## 2. Périmètre de test

| Élément testé | Type de test |
|---|---|
| Frontend Docker | Test de démarrage |
| Page HTML | Test d’accessibilité et de chargement |
| API health | Test d’intégration backend |
| Prédiction simple | Test fonctionnel |
| Prédiction batch | Test fonctionnel |
| Authentification API | Test sécurité |
| Infos modèle | Test fonctionnel |
| Métriques modèle | Test fonctionnel |
| Dashboard monitoring | Test intégration |
| Alertes monitoring | Test intégration |
| Gestion erreurs | Test fonctionnel |

## 3. Préconditions

Avant les tests :

```bash
docker compose up -d --build
```

Services attendus :

```text
paylive_postgres
paylive_pgadmin
paylive_api
paylive_frontend
```

URLs attendues :

```text
Frontend : http://localhost:8080
API      : http://localhost:8000
Swagger  : http://localhost:8000/docs
```

## 4. Tests manuels fonctionnels

## T-01 — Chargement de l’application

| Élément | Description |
|---|---|
| Objectif | Vérifier que le frontend est accessible |
| Action | Ouvrir `http://localhost:8080` |
| Résultat attendu | La page PayLive AI Copilot s’affiche |
| Preuve | Capture d’écran de la page d’accueil |

## T-02 — Test de santé API depuis le frontend

| Élément | Description |
|---|---|
| Objectif | Vérifier que le frontend peut joindre l’API |
| Action | Cliquer sur “Tester l’API” |
| Résultat attendu | Statut API OK affiché |
| Preuve | Capture d’écran du statut |

## T-03 — Prédiction simple valide

| Élément | Description |
|---|---|
| Objectif | Vérifier l’appel IA principal |
| Donnée | `je prends la robe noire en M` |
| Action | Cliquer sur “Analyser” |
| Résultat attendu | Intention prédite affichée |
| Preuve | Capture du résultat |

## T-04 — Commentaire vide

| Élément | Description |
|---|---|
| Objectif | Vérifier la validation côté interface |
| Donnée | Champ commentaire vide |
| Action | Cliquer sur “Analyser” |
| Résultat attendu | Message demandant de saisir un commentaire |
| Preuve | Capture message d’erreur |

## T-05 — Clé API invalide

| Élément | Description |
|---|---|
| Objectif | Vérifier la sécurité API |
| Donnée | Clé API incorrecte |
| Action | Lancer une prédiction |
| Résultat attendu | Message “clé API invalide” |
| Preuve | Capture erreur 403 |

## T-06 — Analyse batch

| Élément | Description |
|---|---|
| Objectif | Vérifier plusieurs prédictions |
| Données | Plusieurs commentaires, un par ligne |
| Action | Cliquer sur “Analyser le lot” |
| Résultat attendu | Tableau avec une ligne par commentaire |
| Preuve | Capture tableau |

## T-07 — Infos modèle

| Élément | Description |
|---|---|
| Objectif | Vérifier l’accès aux métadonnées IA |
| Action | Cliquer sur “Infos modèle” |
| Résultat attendu | Informations du modèle affichées |
| Preuve | Capture section modèle |

## T-08 — Métriques modèle

| Élément | Description |
|---|---|
| Objectif | Vérifier l’accès aux métriques |
| Action | Cliquer sur “Métriques modèle” |
| Résultat attendu | Accuracy, F1 ou rapports affichés |
| Preuve | Capture métriques |

## T-09 — Dashboard monitoring

| Élément | Description |
|---|---|
| Objectif | Vérifier l’accès au dashboard IA |
| Action | Cliquer sur “Dashboard monitoring” |
| Résultat attendu | Dashboard HTML ouvert ou affiché |
| Preuve | Capture dashboard |

## T-10 — Alertes monitoring

| Élément | Description |
|---|---|
| Objectif | Vérifier l’accès aux alertes IA |
| Action | Cliquer sur “Télécharger les alertes” |
| Résultat attendu | Fichier CSV téléchargé ou affiché |
| Preuve | Capture ou fichier CSV |

## 5. Tests d’accessibilité manuels

| Test | Résultat attendu |
|---|---|
| Navigation avec Tab | Tous les champs et boutons sont accessibles |
| Activation clavier | Les boutons fonctionnent avec Entrée ou Espace |
| Focus visible | Le focus est visible sur chaque élément interactif |
| Labels | Tous les champs ont un label visible |
| Erreurs | Les erreurs sont textuelles et lisibles |
| Résultats dynamiques | Les résultats sont annoncés via une zone dédiée |
| Contraste | Les textes restent lisibles |
| Responsive | L’interface reste utilisable sur écran réduit |

## 6. Tests techniques par commandes

## 6.1. Vérifier les conteneurs

```bash
docker compose ps
```

Résultat attendu :

```text
paylive_api       running
paylive_frontend  running
paylive_postgres  running
```

## 6.2. Tester l’API

```bash
curl http://127.0.0.1:8000/health
```

Résultat attendu :

```json
{
  "status": "ok"
}
```

Le contenu exact peut varier selon l’implémentation, mais la réponse doit être en HTTP 200.

## 6.3. Tester le frontend

```bash
curl http://127.0.0.1:8080
```

Résultat attendu :

```text
présence du HTML de l’application
```

## 6.4. Tester une prédiction API

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/ai/predict-intent" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: paylive-dev-api-key" \
  -d "{\"comment_text\":\"je prends la robe noire en M\"}"
```

Résultat attendu :

```text
JSON contenant predicted_intent et confidence_score
```

## 7. Tests automatisés envisagés

Une première version de tests automatisés peut être ajoutée dans :

```text
tests/test_frontend.py
```

Objectifs :

- vérifier que le frontend répond en HTTP 200 ;
- vérifier que `index.html` contient les éléments attendus ;
- vérifier que les fichiers `styles.css`, `config.js` et `app.js` sont présents ;
- vérifier que les routes API utilisées sont présentes dans `config.js` ;
- vérifier que l’application n’embarque pas de données réelles.

Exemples de contrôles :

```text
présence du formulaire de prédiction
présence du champ API key
présence de la zone de résultat
présence de la zone d’erreur
présence des boutons modèle, métriques, dashboard et alertes
```

## 8. Rapport de tests prévu

Un rapport pourra être généré dans :

```text
data/application/reports/frontend_test_report.csv
```

Colonnes proposées :

```text
tested_at
test_name
test_type
expected_result
actual_result
status
evidence_path
comment
```

## 9. Intégration CI possible

Le pipeline GitHub Actions pourra être enrichi avec une étape frontend.

Exemple :

```yaml
- name: Build frontend Docker image
  run: docker compose build frontend

- name: Start stack
  run: docker compose up -d

- name: Test frontend health
  run: curl --fail http://127.0.0.1:8080
```

Cette étape permettra de prouver que l’application web est intégrée dans la chaîne de livraison.

## 10. Critères de validation finale

Le Bloc 3 sera validé si :

| Critère | Statut attendu |
|---|---|
| Frontend Docker lancé | OK |
| Interface visible | OK |
| API consommée | OK |
| Authentification envoyée | OK |
| Résultats affichés | OK |
| Erreurs gérées | OK |
| Dashboard accessible | OK |
| Alertes accessibles | OK |
| Accessibilité testée | OK |
| Tests documentés | OK |
| Sources versionnées | OK |

## 11. Preuves à conserver

```text
capture Docker Compose
capture frontend
capture prédiction simple
capture prédiction batch
capture erreur clé API invalide
capture infos modèle
capture métriques modèle
capture dashboard monitoring
capture alertes CSV
logs Docker frontend
rapport de tests frontend
commit Git correspondant
```

## 12. Conclusion

La stratégie de test du Bloc 3 couvre les aspects fonctionnels, techniques, sécurité, accessibilité et intégration.

Elle permet de démontrer que l’application web n’est pas seulement une page statique, mais une interface réellement connectée au service IA développé dans le Bloc 2.
