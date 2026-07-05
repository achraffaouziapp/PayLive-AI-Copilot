# Tests de l’application — Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document décrit la stratégie de test de l’application web du Bloc 3.

Les tests doivent vérifier que l’interface HTML/CSS/JavaScript :

- se lance correctement dans Docker ;
- est servie par Nginx ;
- communique avec l’API FastAPI ;
- envoie la clé API sur les routes protégées ;
- affiche les résultats IA ;
- gère les erreurs utilisateur ;
- donne accès au monitoring ;
- respecte les critères d’accessibilité de base ;
- est intégrée dans la chaîne CI GitHub Actions.

## 2. Périmètre de test

| Élément testé | Type de test | Statut |
|---|---|---|
| Frontend Docker | Test de build et démarrage | Réalisé |
| Page HTML | Test statique et chargement manuel | Réalisé |
| CSS responsive | Test statique | Réalisé |
| JavaScript | Test statique des routes et comportements attendus | Réalisé |
| Proxy Nginx | Test statique de configuration | Réalisé |
| API health | Test d’intégration backend | Réalisé |
| Prédiction simple | Test fonctionnel manuel | Réalisé |
| Authentification API | Test sécurité manuel et automatisé | Réalisé |
| Infos modèle | Test fonctionnel manuel | Réalisé |
| Métriques modèle | Test fonctionnel manuel | Réalisé |
| Dashboard monitoring | Test intégration manuel | Réalisé |
| Alertes monitoring | Test intégration manuel | Réalisé |
| GitHub Actions | Test CI automatisé | Réalisé |

La prédiction batch n’est pas testée dans l’interface Bloc 3 car elle n’a pas été intégrée dans la première version frontend. Elle reste disponible côté API.

## 3. Préconditions

Avant les tests, lancer l’environnement Docker :

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
Frontend : http://127.0.0.1:8080
API      : http://127.0.0.1:8000
Swagger  : http://127.0.0.1:8000/docs
```

Clé API de démonstration locale :

```text
paylive-dev-api-key
```

## 4. Tests manuels fonctionnels

## T-01 — Chargement de l’application

| Élément | Description |
|---|---|
| Objectif | Vérifier que le frontend est accessible |
| Action | Ouvrir `http://127.0.0.1:8080` |
| Résultat attendu | La page PayLive AI Copilot s’affiche |
| Statut | OK |
| Preuve | Capture d’écran de la page d’accueil |

## T-02 — Test de connexion sécurisée avec clé valide

| Élément | Description |
|---|---|
| Objectif | Vérifier que le frontend peut joindre une route IA protégée |
| Donnée | `paylive-dev-api-key` |
| Action | Cliquer sur “Tester la connexion” |
| Route appelée | `GET /api/v1/ai/model-info` |
| Résultat attendu | Message indiquant que l’API IA est disponible et que la clé est valide |
| Statut | OK |
| Preuve | Capture d’écran du message de succès |

## T-03 — Test de connexion sécurisée avec clé invalide

| Élément | Description |
|---|---|
| Objectif | Vérifier que la clé API est réellement contrôlée |
| Donnée | Clé API incorrecte |
| Action | Modifier la clé API puis cliquer sur “Tester la connexion” |
| Route appelée | `GET /api/v1/ai/model-info` |
| Résultat attendu | Message “Clé API invalide” ou erreur 403 |
| Statut | OK |
| Preuve | Capture d’écran de l’erreur |

Ce test a permis de corriger un comportement initial : le bouton testait `/health`, route publique qui répondait toujours OK même avec une mauvaise clé API.

## T-04 — Prédiction simple valide

| Élément | Description |
|---|---|
| Objectif | Vérifier l’appel IA principal |
| Donnée | `je prends la robe noire en M` |
| Action | Cliquer sur “Analyser le commentaire” |
| Route appelée | `POST /api/v1/ai/predict-intent` |
| Résultat attendu | Intention prédite, score de confiance, temps de réponse et version modèle affichés |
| Statut | OK |
| Preuve | Capture du résultat |

## T-05 — Commentaire vide

| Élément | Description |
|---|---|
| Objectif | Vérifier la validation côté interface |
| Donnée | Champ commentaire vide |
| Action | Cliquer sur “Analyser le commentaire” |
| Résultat attendu | Message demandant de saisir un commentaire |
| Statut | OK |
| Preuve | Capture message d’erreur |

## T-06 — Prédiction à faible confiance

| Élément | Description |
|---|---|
| Objectif | Vérifier l’affichage de l’alerte de confiance faible |
| Donnée | Commentaire ambigu ou court |
| Action | Lancer une prédiction |
| Résultat attendu | Message d’avertissement si `is_low_confidence = true` |
| Statut | OK si le cas est reproduit |
| Preuve | Capture du message d’avertissement |

## T-07 — Infos modèle

| Élément | Description |
|---|---|
| Objectif | Vérifier l’accès aux métadonnées IA |
| Action | Cliquer sur “Charger les informations” |
| Route appelée | `GET /api/v1/ai/model-info` |
| Résultat attendu | Informations du modèle affichées en JSON |
| Statut | OK |
| Preuve | Capture section modèle |

## T-08 — Métriques modèle

| Élément | Description |
|---|---|
| Objectif | Vérifier l’accès aux métriques |
| Action | Cliquer sur “Charger les métriques” |
| Route appelée | `GET /api/v1/ai/model-metrics` |
| Résultat attendu | Métriques d’évaluation affichées en JSON |
| Statut | OK |
| Preuve | Capture métriques |

## T-09 — Dashboard monitoring

| Élément | Description |
|---|---|
| Objectif | Vérifier l’accès au dashboard IA depuis le frontend |
| Action | Cliquer sur “Ouvrir le dashboard” |
| Route appelée | `GET /api/v1/ai/monitoring/dashboard` |
| Résultat attendu | Dashboard HTML ouvert dans un nouvel onglet |
| Statut | OK |
| Preuve | Capture dashboard |

## T-10 — Alertes monitoring

| Élément | Description |
|---|---|
| Objectif | Vérifier l’accès aux alertes IA |
| Action | Cliquer sur “Télécharger les alertes CSV” |
| Route appelée | `GET /api/v1/ai/monitoring/alerts` |
| Résultat attendu | Fichier `model_monitoring_alerts.csv` téléchargé |
| Statut | OK |
| Preuve | Capture ou fichier CSV |

## T-11 — Vérification de la mise en page corrigée

| Élément | Description |
|---|---|
| Objectif | Vérifier que les sections JSON ne cassent pas l’interface |
| Action | Charger les informations modèle et les métriques |
| Résultat attendu | Les sections sont affichées l’une sous l’autre, sans débordement horizontal majeur |
| Statut | OK |
| Preuve | Capture de l’interface après correction CSS |

## 5. Tests d’accessibilité manuels

| Test | Résultat attendu | Statut |
|---|---|---|
| Navigation avec Tab | Tous les champs et boutons sont accessibles | À vérifier avec capture ou note |
| Activation clavier | Les boutons fonctionnent avec Entrée ou Espace | À vérifier |
| Focus visible | Le focus est visible sur chaque élément interactif | À vérifier |
| Labels | Tous les champs principaux ont un label visible | OK |
| Erreurs | Les erreurs sont textuelles et lisibles | OK |
| Résultats dynamiques | Les résultats sont affichés dans des zones dédiées | OK |
| Contraste | Les textes restent lisibles | OK |
| Responsive | L’interface reste utilisable sur écran réduit | OK |

Points d’accessibilité intégrés :

```text
lang="fr" ;
balise main ;
labels ;
boutons HTML natifs ;
aria-live="polite" ;
messages textuels ;
interface responsive.
```

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
paylive_pgadmin   running
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
présence du HTML de l’application PayLive AI Copilot
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
JSON contenant predicted_intent, confidence_score et response_time_ms
```

## 6.5. Tester le dashboard via API

```bash
curl -H "X-API-Key: paylive-dev-api-key" \
  -o dashboard.html \
  http://127.0.0.1:8000/api/v1/ai/monitoring/dashboard
```

Résultat attendu :

```text
fichier dashboard.html généré localement
```

## 6.6. Tester les alertes via API

```bash
curl -H "X-API-Key: paylive-dev-api-key" \
  -o alerts.csv \
  http://127.0.0.1:8000/api/v1/ai/monitoring/alerts
```

Résultat attendu :

```text
fichier alerts.csv généré localement
```

## 7. Tests automatisés réalisés

Un fichier de tests statiques a été ajouté :

```text
tests/test_frontend_static.py
```

Ces tests vérifient :

```text
la présence des fichiers frontend ;
les sections obligatoires dans index.html ;
les routes IA utilisées dans app.js ;
la présence de X-API-Key dans les appels ;
la gestion de localStorage ;
la prise en compte de is_low_confidence ;
la correction du test de clé API ;
les règles CSS responsive ;
la configuration proxy Nginx ;
la présence du Dockerfile Nginx.
```

Commande d’exécution :

```bash
pytest tests/test_frontend_static.py -v
```

Résultat attendu :

```text
7 passed
```

## 8. Extrait des contrôles automatisés

Contrôles importants :

```text
index.html contient PayLive AI Copilot ;
index.html contient les boutons de prédiction, modèle, métriques, dashboard et alertes ;
app.js appelle /predict-intent, /model-info, /model-metrics, /monitoring/dashboard et /monitoring/alerts ;
app.js utilise X-API-Key ;
app.js ne teste plus fetch("/health") pour valider la clé API ;
styles.css contient les règles responsive ;
nginx.conf proxifie /api/ vers http://api:8000/api/ ;
Dockerfile utilise nginx.
```

## 9. Intégration dans la CI GitHub Actions

Le pipeline GitHub Actions a été mis à jour pour inclure les tests Bloc 3.

Fichier :

```text
.github/workflows/ai_mlops_ci.yml
```

Étape de tests :

```yaml
- name: Run automated tests
  run: |
    pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py tests/test_frontend_static.py -v
```

Étape de validation Docker frontend :

```yaml
- name: Validate frontend Docker build
  run: |
    docker compose build frontend
```

Le workflow GitHub Actions passe en vert, ce qui prouve que :

```text
le pipeline IA fonctionne ;
les tests backend/IA passent ;
les tests frontend passent ;
l’image Docker frontend peut être construite.
```

## 10. Rapport de tests

Les preuves de tests sont conservées sous plusieurs formes :

```text
sortie Pytest locale ;
statut GitHub Actions en vert ;
captures d’écran de l’application ;
captures d’écran des erreurs gérées ;
captures du dashboard ;
captures Docker Compose ;
commits Git associés.
```

Un rapport CSV spécifique frontend peut être ajouté ultérieurement si nécessaire :

```text
data/application/reports/frontend_test_report.csv
```

Pour ce Bloc 3, la preuve principale repose sur :

```text
tests/test_frontend_static.py ;
GitHub Actions ;
les captures manuelles ;
le fonctionnement de l’application Dockerisée.
```

## 11. Critères de validation finale

Le Bloc 3 est validé si :

| Critère | Statut attendu |
|---|---|
| Frontend Docker lancé | OK |
| Interface visible | OK |
| API consommée | OK |
| Authentification envoyée | OK |
| Mauvaise clé API détectée | OK |
| Résultats IA affichés | OK |
| Erreurs gérées | OK |
| Dashboard accessible | OK |
| Alertes accessibles | OK |
| Accessibilité de base testée | OK |
| Tests frontend automatisés | OK |
| CI GitHub Actions verte | OK |
| Sources versionnées | OK |

## 12. Preuves à conserver

```text
capture Docker Compose avec paylive_frontend ;
capture de la page frontend ;
capture test de connexion clé valide ;
capture test clé API invalide ;
capture prédiction simple ;
capture alerte faible confiance ;
capture infos modèle ;
capture métriques modèle ;
capture dashboard monitoring ;
fichier alertes CSV ;
logs Docker frontend ;
résultat pytest tests/test_frontend_static.py ;
GitHub Actions en vert ;
commit Git correspondant.
```

## 13. Difficultés rencontrées et corrections

| Difficulté | Cause | Correction |
|---|---|---|
| Deux sections JSON affichées sur la même ligne | Mise en page en deux colonnes trop étroite | Passage de `.grid-2` en une seule colonne |
| JSON trop large | Lignes longues non coupées | Ajout de `overflow: auto`, `white-space: pre-wrap` et `word-break` |
| Test API toujours OK avec mauvaise clé | Le bouton testait `/health`, route publique | Remplacement par un test sur `/model-info`, route protégée |
| Besoin de preuve CI frontend | CI initialement centrée sur l’IA | Ajout des tests frontend et du build Docker frontend dans GitHub Actions |

## 14. Conclusion

La stratégie de test du Bloc 3 couvre les aspects :

```text
fonctionnels ;
sécurité ;
interface ;
accessibilité ;
Docker ;
intégration API ;
monitoring ;
CI/CD.
```

Les tests démontrent que l’application web n’est pas seulement une page statique. Elle consomme réellement le service IA développé dans le Bloc 2, affiche les résultats, gère l’authentification et donne accès aux éléments de monitoring.

Le passage de GitHub Actions en vert confirme que le frontend est intégré dans la chaîne de qualité du projet.
