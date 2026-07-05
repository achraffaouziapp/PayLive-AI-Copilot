# Incidents, corrections et maintenance — Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document recense les incidents techniques rencontrés pendant le Bloc 3, les corrections appliquées et les procédures de maintenance associées.

L’objectif est de prouver que les anomalies ont été diagnostiquées, corrigées, testées et documentées.

## 2. Périmètre

Le périmètre couvre :

- l’application frontend HTML/CSS/JavaScript ;
- le conteneur Docker/Nginx du frontend ;
- l’intégration avec l’API FastAPI ;
- les appels sécurisés par `X-API-Key` ;
- l’accès au dashboard IA ;
- les tests automatisés ;
- la CI GitHub Actions.

## 3. Outil de suivi des incidents

Les incidents sont suivis dans Jira sous forme de tickets de type :

```text
Bug
```

Chaque bug contient :

- un titre ;
- une description ;
- les étapes de reproduction ;
- le résultat observé ;
- le résultat attendu ;
- la correction appliquée ;
- les tests de non-régression ;
- le statut final.

## 4. Incidents identifiés et corrigés

## 4.1. Incident PAYLIVE-47 — Sections modèle et métriques affichées sur la même ligne

| Élément | Description |
|---|---|
| Type | Bug |
| Gravité | Moyenne |
| Composant | Frontend CSS |
| Fichier concerné | `frontend/css/styles.css` |
| Symptôme | Les blocs “Informations modèle” et “Métriques modèle” étaient affichés côte à côte, ce qui rendait le JSON trop large et peu lisible. |
| Cause | La classe `.grid-2` utilisait deux colonnes au lieu d’une disposition verticale. |
| Correction | Modification de `.grid-2` avec `grid-template-columns: 1fr`. Ajout de règles pour éviter le débordement du JSON. |
| Test réalisé | Rechargement du frontend, vérification visuelle, test statique CSS. |
| Statut | Corrigé |

Correction appliquée :

```css
.grid-2 {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

.json-output {
  overflow: auto;
  max-height: 420px;
  white-space: pre-wrap;
  word-break: break-word;
}
```

## 4.2. Incident PAYLIVE-48 — Le test de connexion acceptait une clé API invalide

| Élément | Description |
|---|---|
| Type | Bug |
| Gravité | Haute |
| Composant | Frontend JavaScript |
| Fichier concerné | `frontend/js/app.js` |
| Symptôme | En saisissant une mauvaise clé API puis en cliquant sur “Tester la connexion”, l’application affichait quand même que l’API était disponible. |
| Cause | Le bouton testait la route publique `/health`, qui ne nécessite pas de clé API. |
| Correction | Le test de connexion utilise maintenant la route protégée `/api/v1/ai/model-info`. |
| Test réalisé | Test avec clé valide, test avec clé invalide, test automatisé dans `tests/test_frontend_static.py`. |
| Statut | Corrigé |

Logique corrigée :

```javascript
const response = await fetch(`${getApiBaseUrl()}/model-info`, {
  method: "GET",
  headers: getHeaders(),
});

if (response.status === 401) {
  throw new Error("Clé API absente.");
}

if (response.status === 403) {
  throw new Error("Clé API invalide.");
}
```

## 4.3. Incident — Vérification du dashboard depuis le frontend

| Élément | Description |
|---|---|
| Type | Intégration |
| Gravité | Moyenne |
| Composant | Frontend + API IA |
| Fichiers concernés | `frontend/js/app.js`, `api/routes/ai.py` |
| Symptôme | L’accès au dashboard nécessitait l’envoi de la clé API dans les headers. |
| Cause | Les routes de monitoring IA sont protégées par `X-API-Key`. |
| Correction | L’appel JavaScript au dashboard envoie explicitement le header `X-API-Key`. |
| Test réalisé | Ouverture du dashboard depuis le frontend, téléchargement des alertes CSV. |
| Statut | Validé |

## 5. Tests de non-régression

Après correction, les tests suivants ont été réalisés :

```bash
pytest tests/test_frontend_static.py -v
```

Puis :

```bash
pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py tests/test_frontend_static.py -v
```

Le pipeline GitHub Actions a également été exécuté après push et est passé en vert.

## 6. Procédures de diagnostic

## 6.1. Vérifier les conteneurs

```bash
docker compose ps
```

Services attendus :

```text
paylive_frontend
paylive_api
paylive_postgres
paylive_pgadmin
```

## 6.2. Lire les logs du frontend

```bash
docker logs --tail 80 paylive_frontend
```

## 6.3. Lire les logs de l’API

```bash
docker logs --tail 80 paylive_api
```

## 6.4. Tester le frontend

```bash
curl http://127.0.0.1:8080
```

Résultat attendu :

```text
HTML de l’application PayLive AI Copilot
```

## 6.5. Tester l’API

```bash
curl http://127.0.0.1:8000/health
```

Résultat attendu :

```text
réponse HTTP 200
```

## 6.6. Tester une route protégée

```bash
curl -H "X-API-Key: paylive-dev-api-key" http://127.0.0.1:8000/api/v1/ai/model-info
```

Résultat attendu :

```text
réponse HTTP 200 avec les informations du modèle IA
```

## 7. Procédure de maintenance frontend

En cas de modification de l’interface :

1. modifier les fichiers dans `frontend/` ;
2. reconstruire le conteneur frontend ;
3. tester l’application dans le navigateur ;
4. lancer les tests automatisés ;
5. vérifier GitHub Actions après push.

Commandes :

```bash
docker compose up -d --build frontend
pytest tests/test_frontend_static.py -v
git status
```

## 8. Procédure de maintenance API / intégration IA

En cas de modification des routes API IA :

1. vérifier que les routes restent disponibles dans Swagger ;
2. vérifier que la clé API est toujours nécessaire ;
3. tester les appels depuis le frontend ;
4. lancer les tests API ;
5. vérifier les logs Docker.

Commandes :

```bash
pytest tests/test_ai_api.py -v
docker logs --tail 80 paylive_api
```

## 9. Procédure de rollback

En cas de régression :

```bash
git log --oneline
git checkout <commit_precedent>
docker compose up -d --build
pytest tests/test_frontend_static.py -v
```

Si la correction doit être annulée par commit :

```bash
git revert <commit_a_annuler>
git push
```

## 10. Bonnes pratiques OWASP appliquées

Les mesures suivantes sont appliquées au Bloc 3 :

| Risque | Mesure appliquée |
|---|---|
| Accès non autorisé | Envoi obligatoire de `X-API-Key` pour les routes IA protégées |
| Mauvaise validation des accès | Le bouton de test utilise une route protégée |
| Exposition excessive de données | L’interface affiche uniquement les informations nécessaires |
| Erreurs non lisibles | Les erreurs sont affichées sous forme textuelle |
| Données sensibles dans le projet | Aucune donnée PayLive réelle n’est utilisée |
| Configuration locale | La clé API préremplie est uniquement destinée à la démonstration locale |
| Dépendance frontend/API | Nginx proxifie les appels vers le backend dans Docker |

## 11. Preuves à conserver

Les preuves recommandées sont :

```text
capture Jira du ticket PAYLIVE-47
capture Jira du ticket PAYLIVE-48
capture du frontend corrigé
capture du test clé API invalide
capture des tests pytest en succès
capture GitHub Actions en vert
capture docker compose ps
capture dashboard monitoring ouvert depuis le frontend
```

## 12. Conclusion

Les incidents rencontrés pendant le Bloc 3 ont été diagnostiqués, corrigés et testés.

Les corrections principales concernent l’ergonomie de l’interface et la validation réelle de la clé API.

La maintenance est facilitée par Docker, les logs, les tests automatisés, GitHub Actions et le suivi Jira des tickets.
