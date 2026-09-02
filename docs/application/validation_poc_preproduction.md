# 35 — Validation du POC en environnement de pré-production

## 1. Environnement validé

```text
Environnement :
Pré-production locale conteneurisée

Frontend :
http://127.0.0.1:8081

API :
http://127.0.0.1:8001

Documentation OpenAPI :
http://127.0.0.1:8001/docs

Version applicative :
1.0.0

Version modèle :
intent_classifier_v1

Base PostgreSQL :
paylive_ai_copilot_preprod

Date de validation :
02/09/2026
```

La pré-production est distincte de l’environnement de développement grâce à :

- `docker-compose.preprod.yml` ;
- `.env.preprod` ;
- ports dédiés ;
- base PostgreSQL dédiée ;
- volume PostgreSQL dédié ;
- lancement Uvicorn sans `--reload` ;
- absence de bind mount applicatif ;
- health checks Docker pour PostgreSQL, API et frontend.

---

## 2. Architecture de pré-production

```text
Navigateur
   ↓
Frontend Nginx
http://127.0.0.1:8081
   ↓
API FastAPI
http://127.0.0.1:8001
   ↓
Service IA
   ↓
TF-IDF + Logistic Regression
   ↓
PostgreSQL
paylive_ai_copilot_preprod
```

Services Docker :

```text
paylive_preprod_postgres
paylive_preprod_api
paylive_preprod_frontend
```

---

## 3. Résultats des smoke tests

| ID | Test | Résultat | Preuve / observation |
|---|---|---|---|
| ST-01 | Services Docker | **PASS** | PostgreSQL, API et frontend en état `healthy` |
| ST-02 | Frontend accessible | **PASS** | `HTTP 200` sur `http://127.0.0.1:8081/` |
| ST-03 | API accessible | **PASS** | `HTTP 200` sur `http://127.0.0.1:8001/` |
| ST-04 | Health check | **PASS** | `HTTP 200`, `status: ok`, base `paylive_ai_copilot_preprod` disponible |
| ST-05 | Route protégée sans clé | **PASS** | `HTTP 401 Unauthorized` |
| ST-06 | Clé API invalide | **PASS** | `HTTP 403 Forbidden` |
| ST-07 | Clé valide / model-info | **PASS** | `HTTP 200`, modèle `intent_classifier_v1` chargé |
| ST-08 | Prédiction IA | **PASS** | prédiction retournée avec intention, confiance, temps de réponse et version modèle |
| ST-09 | Frontend → API | **PASS** | prédiction réussie depuis le frontend de pré-production |
| ST-10 | CORS | **PASS** | `HTTP 200`, origine `http://127.0.0.1:8081`, POST et `X-API-Key` autorisés |

---

## 4. Détail des validations observées

### Frontend

Le frontend de pré-production répond correctement :

```text
HTTP/1.1 200 OK
Server: nginx/1.27.5
```

URL :

```text
http://127.0.0.1:8081
```

### API

La racine de l’API répond correctement :

```text
HTTP/1.1 200 OK
```

avec notamment :

```json
{
  "application": "PayLive AI Copilot API",
  "version": "1.0.0",
  "documentation_url": "/docs",
  "health_url": "/health"
}
```

### Health check

Le health check confirme la disponibilité de l’API et de la base de pré-production :

```text
HTTP 200
status: ok
database_available: true
database_name: paylive_ai_copilot_preprod
```

### Sécurité

Sans clé API :

```text
HTTP 401 Unauthorized
```

Avec une clé invalide :

```text
HTTP 403 Forbidden
```

Avec une clé valide :

```text
HTTP 200 OK
```

La valeur réelle de la clé n’est pas consignée dans ce document.

### Modèle IA

Le service retourne les informations du modèle :

```text
model_name:
intent_classifier

model_version:
intent_classifier_v1

algorithm:
TF-IDF + Logistic Regression

test_accuracy:
0.8

test_macro_f1:
0.6

test_weighted_f1:
0.72
```

### Prédiction IA

Une prédiction a été exécutée avec succès.

Exemple observé :

```text
comment_text:
je prends la robe noire en M

predicted_intent:
purchase_intent

confidence_score:
0.25

model_version:
intent_classifier_v1

response_time_ms:
5.52

is_low_confidence:
true

low_confidence_threshold:
0.6
```

### CORS

Le preflight CORS de la pré-production répond :

```text
HTTP 200
```

avec :

```text
access-control-allow-methods:
GET, POST, OPTIONS

access-control-allow-headers:
Content-Type, X-API-Key

access-control-allow-origin:
http://127.0.0.1:8081
```

### Validation frontend → API

Une prédiction a également été réalisée avec succès depuis l’interface disponible sur :

```text
http://127.0.0.1:8081
```

Cela valide la chaîne fonctionnelle :

```text
Frontend
↓
API
↓
Service IA
↓
Modèle
↓
Résultat affiché
```

---

## 5. Version Git validée

À renseigner avec :

```cmd
git rev-parse HEAD
```

```text
Commit Git :
3edd0d0d97542fcc0dd35332e9bac57b1160bf2e
```

---

## 6. Preuves à conserver

Captures recommandées :

```text
preuve_c15_preprod_compose_ps.png
preuve_c15_preprod_frontend_200.png
preuve_c15_preprod_api_200.png
preuve_c15_preprod_health.png
preuve_c15_preprod_auth_401.png
preuve_c15_preprod_auth_403.png
preuve_c15_preprod_model_info.png
preuve_c15_preprod_prediction_api.png
preuve_c15_preprod_prediction_frontend.png
preuve_c15_preprod_cors.png
preuve_c15_preprod_commit.png
```

Fichiers de configuration à conserver :

```text
docker-compose.preprod.yml
.env.preprod.example
docs/08_application/35_validation_poc_preproduction.md
```

Le fichier réel `.env.preprod` ne doit pas être publié s’il contient des secrets.

---

## 7. Conclusion POC

```text
Conclusion POC :
GO
```

La preuve de concept est considérée comme **validée dans l’environnement de pré-production locale conteneurisée**.

Les fonctionnalités principales ont été vérifiées :

- démarrage isolé des services ;
- disponibilité du frontend ;
- disponibilité de l’API ;
- connexion PostgreSQL ;
- sécurité par clé API ;
- chargement du modèle ;
- prédiction IA ;
- communication frontend/API ;
- politique CORS adaptée à la pré-production.

La décision `GO` signifie ici :

```text
GO pour la validation du POC dans l’environnement de pré-production.
```

Elle ne constitue pas une décision de mise en production publique.

---

## 8. Limites avant une production réelle

Les améliorations suivantes resteraient nécessaires pour une mise en production publique :

- hébergement distant avec URL publique ;
- gestion des secrets par un gestionnaire dédié ;
- authentification plus avancée si nécessaire ;
- supervision applicative centralisée ;
- stratégie de sauvegarde et restauration ;
- stratégie de rollback ;
- contrôle de charge ;
- durcissement de la configuration réseau ;
- utilisation d’une clé API spécifiquement dédiée à la pré-production et à la production.

---

## 9. Synthèse finale

```text
Environnement :
Pré-production locale conteneurisée

URL frontend :
http://127.0.0.1:8081

URL API :
http://127.0.0.1:8001

Version :
1.0.0

Version modèle :
intent_classifier_v1

Date de validation :
02/09/2026

Tests smoke :
10 / 10 PASS

Conclusion POC :
GO

Périmètre du GO :
validation du POC en pré-production locale, hors mise en production publique
```
