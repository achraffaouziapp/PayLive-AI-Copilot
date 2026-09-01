# 35 — Validation du POC en environnement de pré-production

## 1. Objectif

Cette fiche formalise la validation de la preuve de concept dans un environnement de pré-production réellement hébergé.

L'objectif est de vérifier que l'application est accessible depuis Internet, que le frontend communique avec l'API déployée, que le modèle IA est chargé dans l'image publiée et que les fonctionnalités principales sont utilisables hors de l'environnement local de développement.

Aucune valeur de validation ne doit être renseignée avant l'exécution réelle des tests.

---

## 2. Identification de l'environnement

| Élément | Valeur |
|---|---|
| Environnement | Pré-production / Staging |
| Hébergeur | Render |
| URL frontend | À renseigner après déploiement |
| URL API | À renseigner après déploiement |
| Branche | main / master |
| Commit Git validé | À renseigner |
| Image GHCR | À renseigner |
| Tag / SHA image | À renseigner |
| Version applicative | À renseigner |
| Version du modèle | À renseigner à partir de `/api/v1/ai/model-info` |
| Date de validation | À renseigner après test |

---

## 3. Architecture de pré-production

```text
GitHub
   ↓
GitHub Actions / MLOps
   ↓
GHCR — image API + modèle
   ↓
Render Web Service
   ↓
API FastAPI publique HTTPS

GitHub
   ↓
Render Static Site
   ↓
Frontend HTML / CSS / JavaScript public HTTPS
   ↓
API de pré-production
```

Le frontend et l'API utilisent deux URLs publiques distinctes. Le domaine du frontend est autorisé explicitement dans la configuration CORS de l'API avec la variable :

```text
ALLOWED_ORIGINS=<URL_FRONTEND_PREPROD>
```

---

## 4. Configuration API de pré-production

Variables minimales :

```text
ENVIRONMENT=preproduction
API_KEY=<SECRET_PREPROD>
ALLOWED_ORIGINS=<URL_FRONTEND_PREPROD>
```

La clé API est définie dans l'hébergeur et n'est pas stockée en clair dans le dépôt Git.

Commande de démarrage recommandée pour le conteneur :

```text
python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

Image :

```text
ghcr.io/<github-owner>/paylive-ai-api:<commit-sha>
```

L'utilisation du SHA Git permet d'associer précisément l'environnement validé à une version du code et de l'image.

---

## 5. Configuration frontend de pré-production

Le frontend statique est déployé depuis :

```text
frontend/
```

L'URL de base de l'API configurée dans l'interface doit être :

```text
https://<URL_API_PREPROD>/api/v1/ai
```

La clé utilisée pendant la validation doit être la clé API de pré-production.

---

## 6. Smoke tests

### ST-01 — Frontend accessible

Action :

```text
ouvrir l'URL publique du frontend
```

Résultat attendu :

```text
HTTP 200 et interface affichée
```

Résultat réel :

```text
À renseigner : PASS / FAIL
```

### ST-02 — API accessible

Commande :

```cmd
curl -i https://<URL_API_PREPROD>/
```

Résultat attendu :

```text
HTTP 200
```

Résultat réel :

```text
À renseigner : PASS / FAIL
```

### ST-03 — Health check

Commande :

```cmd
curl -i https://<URL_API_PREPROD>/health
```

Résultat attendu :

```text
HTTP 200
```

Résultat réel :

```text
À renseigner : PASS / FAIL
```

### ST-04 — Sécurité sans clé API

Commande :

```cmd
curl -i https://<URL_API_PREPROD>/api/v1/ai/model-info
```

Résultat attendu :

```text
HTTP 401
```

Résultat réel :

```text
À renseigner : PASS / FAIL
```

### ST-05 — Sécurité avec clé invalide

Commande :

```cmd
curl -i -H "X-API-Key: invalid-preprod-key" https://<URL_API_PREPROD>/api/v1/ai/model-info
```

Résultat attendu :

```text
HTTP 403
```

Résultat réel :

```text
À renseigner : PASS / FAIL
```

### ST-06 — Chargement du modèle

Commande :

```cmd
curl -i -H "X-API-Key: <CLE_PREPROD>" https://<URL_API_PREPROD>/api/v1/ai/model-info
```

Résultat attendu :

```text
HTTP 200
```

La réponse doit permettre d'identifier le modèle ou sa version.

Résultat réel :

```text
À renseigner : PASS / FAIL
```

### ST-07 — Prédiction IA

Commande :

```cmd
curl -X POST https://<URL_API_PREPROD>/api/v1/ai/predict-intent -H "Content-Type: application/json" -H "X-API-Key: <CLE_PREPROD>" -d "{\"comment_text\":\"je prends la robe noire en M\"}"
```

Résultat attendu :

```text
HTTP 200
predicted_intent présent
confidence_score présent
response_time_ms présent
model_version présent
```

Résultat réel :

```text
À renseigner : PASS / FAIL
```

### ST-08 — Métriques du modèle

Commande :

```cmd
curl -i -H "X-API-Key: <CLE_PREPROD>" https://<URL_API_PREPROD>/api/v1/ai/model-metrics
```

Résultat attendu :

```text
HTTP 200
```

Résultat réel :

```text
À renseigner : PASS / FAIL
```

### ST-09 — Test frontend → API

Depuis l'interface de pré-production :

```text
1. renseigner l'URL API de pré-production ;
2. renseigner la clé API de pré-production ;
3. tester la connexion ;
4. saisir un commentaire ;
5. lancer une prédiction ;
6. consulter le résultat ;
7. charger les informations du modèle ;
8. charger les métriques.
```

Résultat attendu :

```text
aucune erreur CORS ;
connexion API réussie ;
prédiction affichée ;
informations du modèle affichées.
```

Résultat réel :

```text
À renseigner : PASS / FAIL
```

### ST-10 — Monitoring

Depuis l'interface ou l'API :

```text
dashboard monitoring
alertes monitoring
```

Résultat attendu :

```text
les ressources de monitoring sont accessibles avec une clé valide.
```

Résultat réel :

```text
À renseigner : PASS / FAIL
```

---

## 7. Tableau de synthèse

| Test | Résultat |
|---|---|
| Frontend public accessible | À renseigner |
| API publique accessible | À renseigner |
| Health check | À renseigner |
| Authentification sans clé | À renseigner |
| Authentification clé invalide | À renseigner |
| `model-info` | À renseigner |
| Prédiction IA | À renseigner |
| Métriques modèle | À renseigner |
| Frontend → API sans erreur CORS | À renseigner |
| Monitoring | À renseigner |

---

## 8. Preuves à conserver

Captures recommandées :

```text
preuve_c15_render_frontend.png
preuve_c15_render_api.png
preuve_c15_url_frontend.png
preuve_c15_url_api.png
preuve_c15_smoke_health.png
preuve_c15_smoke_model_info.png
preuve_c15_smoke_predict.png
preuve_c15_frontend_prediction.png
preuve_c15_version_sha.png
preuve_c15_validation_complete.png
```

Conserver également :

- capture Render montrant le service API déployé ;
- capture Render montrant le Static Site déployé ;
- commit Git validé ;
- URL ou référence de l'image GHCR ;
- résultat des smoke tests ;
- version du modèle retournée par `model-info`.

---

## 9. Anomalies rencontrées

| ID | Anomalie | Impact | Correction | Retest |
|---|---|---|---|---|
| PREPROD-01 | À renseigner si nécessaire | À renseigner | À renseigner | PASS / FAIL |

Si aucune anomalie n'est observée :

```text
Aucune anomalie bloquante observée pendant la validation.
```

---

## 10. Conclusion POC

### Décision

```text
GO / NO GO / GO SOUS CONDITIONS
```

### Justification

À rédiger uniquement après l'exécution des tests.

Exemple de structure :

```text
La preuve de concept a été déployée et testée dans un environnement
de pré-production accessible publiquement.

X/X smoke tests sont concluants.

Les fonctionnalités principales frontend → API → modèle IA sont
fonctionnelles / présentent les anomalies suivantes : ...

Décision : GO / NO GO / GO sous conditions.
```

### Conditions éventuelles avant production

Selon les résultats, les points suivants peuvent être retenus :

- renforcer la gestion des secrets ;
- augmenter la couverture de tests ;
- industrialiser le monitoring ;
- ajouter un environnement PostgreSQL si les fonctionnalités métier correspondantes doivent être validées ;
- prévoir une stratégie de rollback ;
- configurer un domaine et une politique HTTPS de production ;
- effectuer une nouvelle validation avec des données autorisées représentatives.

---

## 11. Résultat final à compléter

```text
Environnement : Pré-production / Staging Render

URL frontend :
URL API :

Version applicative :
Commit Git :
Image GHCR :
Version modèle :

Date de validation :

Nombre de smoke tests :
Tests PASS :
Tests FAIL :

Conclusion POC :
GO / NO GO / GO SOUS CONDITIONS

Commentaire final :
```
