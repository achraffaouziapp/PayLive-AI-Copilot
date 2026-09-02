# Monitoring applicatif

## 1. Objectif

Le monitoring applicatif complète le monitoring du modèle IA. Il suit le fonctionnement de l'application elle-même : disponibilité, trafic HTTP, erreurs et latence.

Le monitoring du modèle reste séparé dans `data/ai/`. Le monitoring applicatif utilise `data/application_monitoring/`.

## 2. Métriques suivies

| Métrique | Description |
|---|---|
| API availability | disponibilité de la route de santé de l'API |
| Frontend availability | disponibilité HTTP du frontend |
| HTTP latency | durée des requêtes reçues par FastAPI |
| Request count | nombre de requêtes HTTP observées |
| HTTP 5xx rate | part des réponses serveur 5xx |
| API errors | nombre de réponses HTTP avec statut `>= 400` |

## 3. Collecte automatique

Chaque requête réelle reçue par FastAPI traverse le middleware :

```text
requête HTTP
↓
application_monitoring_middleware
↓
mesure méthode / route / statut / latence
↓
data/application_monitoring/app_metrics.csv
```

Schéma :

```csv
timestamp,method,path,status_code,response_time_ms,is_5xx,error_type
```

Une erreur d'écriture du fichier de monitoring est journalisée mais ne doit pas rendre l'API indisponible.

## 4. Seuils d'alerte

| Condition | Niveau | Code |
|---|---|---|
| latence HTTP moyenne `> 1000 ms` | WARNING | `APP_API_LATENCY_HIGH` |
| taux HTTP 5xx `> 5 %` | CRITICAL | `APP_HTTP_5XX_RATE_HIGH` |
| API indisponible | CRITICAL | `APP_API_UNAVAILABLE` |
| frontend indisponible | CRITICAL | `APP_FRONTEND_UNAVAILABLE` |

## 5. Fichiers générés

```text
data/application_monitoring/
├── app_metrics.csv
├── app_alerts.csv
├── app_summary.json
└── app_monitoring_dashboard.html
```

`app_summary.json` est un fichier intermédiaire utilisé par le générateur du dashboard.

## 6. Disponibilité API et frontend

Valeurs locales par défaut :

```text
APPLICATION_MONITORING_API_URL=http://127.0.0.1:8000/health
APPLICATION_MONITORING_FRONTEND_URL=http://127.0.0.1:8080/
```

En pré-production, les variables peuvent pointer vers les URLs Render réelles.

## 7. Exécution locale

Démarrer l'application :

```cmd
docker compose up -d postgres api frontend
```

Générer du trafic réel :

```cmd
curl -i http://127.0.0.1:8000/
curl -i http://127.0.0.1:8000/health
curl -i -H "X-API-Key: paylive-dev-api-key" http://127.0.0.1:8000/api/v1/ai/model-info
```

Afficher les métriques :

```cmd
type data\application_monitoring\app_metrics.csv
```

Analyser les métriques et vérifier la disponibilité :

```cmd
python -m src.application_monitoring.analyze_application_monitoring
```

Générer le dashboard :

```cmd
python -m src.application_monitoring.generate_application_monitoring_dashboard
```

Ouvrir le dashboard :

```cmd
start data\application_monitoring\app_monitoring_dashboard.html
```

## 8. Tests automatisés

```cmd
python -m pytest tests\test_application_monitoring_middleware.py tests\test_application_monitoring_analysis.py tests\test_application_monitoring_dashboard.py -v
```

Les tests couvrent notamment :

- écriture d'une métrique après une requête réussie ;
- détection d'un statut 5xx ;
- journalisation d'une exception non gérée ;
- absence d'impact applicatif si l'écriture monitoring échoue ;
- branchement du middleware dans `api.main` ;
- calcul du volume, de la latence et du taux 5xx ;
- alerte de latence au-dessus de 1000 ms ;
- alerte critique si le taux 5xx dépasse 5 % ;
- alerte critique si l'API est indisponible ;
- alerte critique si le frontend est indisponible ;
- génération d'un dashboard HTML contenant un tableau accessible.

## 9. Validation des alertes

Scénarios contrôlés recommandés :

```cmd
python -m pytest tests\test_application_monitoring_analysis.py::test_latency_above_1000ms_creates_warning -v
python -m pytest tests\test_application_monitoring_analysis.py::test_5xx_rate_above_5_percent_creates_critical -v
python -m pytest tests\test_application_monitoring_analysis.py::test_unavailable_api_creates_critical -v
python -m pytest tests\test_application_monitoring_analysis.py::test_unavailable_frontend_creates_critical -v
```

Ces scénarios sont des tests contrôlés. Ils ne doivent pas être présentés comme des incidents historiques réels.

## 10. Dashboard

Le dashboard affiche :

- disponibilité API ;
- disponibilité frontend ;
- nombre de requêtes ;
- nombre et taux de HTTP 5xx ;
- latence HTTP moyenne ;
- latence HTTP maximale ;
- nombre d'erreurs API ;
- alertes actives.

Les alertes sont également présentées dans un tableau HTML avec en-têtes et légendes afin que l'information ne repose pas uniquement sur une représentation visuelle.

## 11. Limites du POC

Le stockage CSV est adapté à une preuve de concept mono-processus. Pour une application distribuée ou plusieurs workers Uvicorn, une solution centralisée telle que Prometheus/OpenTelemetry serait plus adaptée.

Sur un hébergement à système de fichiers éphémère, les métriques doivent être exportées vers un stockage persistant si une conservation longue durée est requise.

## 12. Preuves C20 à conserver

```text
capture_app_metrics_csv.png
capture_app_alerts_csv.png
capture_app_monitoring_dashboard.png
capture_latency_warning.png
capture_5xx_alert.png
capture_api_unavailable_alert.png
capture_frontend_unavailable_alert.png
capture_application_monitoring_tests.png
```

## 13. Conclusion

Le dispositif distingue clairement le suivi du modèle IA du suivi de l'application. Les requêtes HTTP sont mesurées automatiquement et les métriques sont agrégées pour suivre la disponibilité, la latence, le volume de trafic et les erreurs. Les seuils définis permettent de produire des alertes explicites et un dashboard de synthèse.

La validation finale de C20 doit reposer sur les résultats réellement obtenus après exécution des tests et génération des fichiers dans le projet.
