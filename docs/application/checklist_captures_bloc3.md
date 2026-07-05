# Checklist des captures d’écran — Bloc 3

## 1. Interface

- [ ] Page frontend sur `http://127.0.0.1:8080`
- [ ] Section Configuration API
- [ ] Section Prédiction d’intention
- [ ] Section Informations modèle
- [ ] Section Métriques modèle
- [ ] Section Monitoring IA

Nom conseillé :

```text
screen_bloc3_01_frontend_accueil.png
```

## 2. Sécurité API

- [ ] Test avec clé API valide
- [ ] Test avec clé API invalide

Noms conseillés :

```text
screen_bloc3_02_api_key_valide.png
screen_bloc3_03_api_key_invalide.png
```

## 3. Prédiction IA

Commentaire conseillé :

```text
je prends la robe noire en M
```

Captures :

- [ ] commentaire saisi
- [ ] intention prédite affichée
- [ ] score de confiance affiché
- [ ] temps de réponse affiché
- [ ] version modèle affichée

Nom conseillé :

```text
screen_bloc3_04_prediction_intention.png
```

## 4. Faible confiance

Commentaire possible :

```text
ok merci
```

Capture :

- [ ] message de faible confiance si affiché

Nom conseillé :

```text
screen_bloc3_05_faible_confiance.png
```

## 5. Modèle IA

Captures :

- [ ] informations modèle
- [ ] métriques modèle

Noms conseillés :

```text
screen_bloc3_06_model_info.png
screen_bloc3_07_model_metrics.png
```

## 6. Monitoring

Captures :

- [ ] dashboard monitoring ouvert depuis le frontend
- [ ] fichier alertes CSV téléchargé ou ouvert

Noms conseillés :

```text
screen_bloc3_08_dashboard_monitoring.png
screen_bloc3_09_alertes_csv.png
```

## 7. Docker

Commandes :

```bash
docker ps
docker compose ps
```

Captures :

- [ ] `paylive_frontend`
- [ ] `paylive_api`
- [ ] `paylive_postgres`
- [ ] `paylive_pgadmin`

Noms conseillés :

```text
screen_bloc3_10_docker_ps.png
screen_bloc3_11_docker_compose_ps.png
```

## 8. Tests

Commandes :

```bash
pytest tests/test_frontend_static.py -v
pytest tests/test_ai_dataset.py tests/test_intent_model.py tests/test_ai_api.py tests/test_frontend_static.py -v
```

Captures :

- [ ] tests frontend passés
- [ ] tests complets passés

Noms conseillés :

```text
screen_bloc3_12_tests_frontend.png
screen_bloc3_13_tests_complets.png
```

## 9. GitHub Actions

Captures :

- [ ] workflow `AI MLOps CI` en vert
- [ ] étape `Run automated tests`
- [ ] étape `Validate frontend Docker build`

Noms conseillés :

```text
screen_bloc3_14_github_actions_vert.png
screen_bloc3_15_ci_docker_build_frontend.png
```

## 10. Code et architecture

Captures :

- [ ] structure `frontend/`
- [ ] code `fetch(.../predict-intent)`
- [ ] proxy Nginx `proxy_pass http://api:8000/api/`
- [ ] service `frontend` dans `docker-compose.yml`

Noms conseillés :

```text
screen_bloc3_16_structure_frontend.png
screen_bloc3_17_code_fetch_prediction.png
screen_bloc3_18_nginx_proxy.png
screen_bloc3_19_docker_compose_frontend.png
```

## 11. Organisation dans le dossier

Les captures peuvent être regroupées ainsi :

```text
1. Interface utilisateur
2. Sécurité API
3. Prédiction IA
4. Monitoring
5. Docker
6. Tests et CI
7. Architecture technique
```

Chaque capture doit être accompagnée d’une courte phrase expliquant ce qu’elle prouve.
