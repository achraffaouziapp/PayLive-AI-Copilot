# Monitoring du modèle IA — PayLive AI Copilot

## 1. Objectif du document

Ce document décrit le monitoring mis en place pour le modèle IA du projet **PayLive AI Copilot** ainsi que sa validation en environnement de test.

Le monitoring permet de suivre les prédictions réalisées par le service IA, de produire des indicateurs sur son fonctionnement, de détecter certaines situations à surveiller et de restituer ces informations sous forme de rapports, d'alertes et d'un dashboard HTML.

## 2. Objectif du monitoring

Le monitoring répond à plusieurs objectifs :

- historiser les prédictions ;
- suivre le nombre de prédictions ;
- suivre les classes prédites ;
- suivre les scores de confiance ;
- identifier les prédictions incertaines ;
- suivre les temps de réponse ;
- suivre la version du modèle utilisée ;
- détecter certaines situations nécessitant une surveillance ;
- produire un rapport et un dashboard exploitables pour le dossier professionnel.

## 3. Script principal de monitoring

Le script principal est :

```text
src/ai/monitoring/monitor_predictions.py
```

Il permet :

- d'enregistrer une prédiction ;
- d'enregistrer un batch de prédictions ;
- de lire le log existant ;
- de générer un rapport de monitoring ;
- de générer les alertes associées aux seuils définis.

Le dashboard est généré avec :

```text
src/ai/monitoring/generate_monitoring_dashboard.py
```

## 4. Fichiers générés

Le monitoring produit les artefacts suivants :

```text
data/ai/predictions/ai_predictions_log.csv
data/ai/reports/model_monitoring_report.csv
data/ai/reports/model_monitoring_dashboard.html
data/ai/reports/model_monitoring_alerts.csv
```

Le fichier `ai_predictions_log.csv` constitue la source de traçabilité des prédictions. Le rapport CSV, le dashboard HTML et le fichier d'alertes sont régénérés à partir des données disponibles.

## 5. Log des prédictions

Le fichier de log est :

```text
data/ai/predictions/ai_predictions_log.csv
```

Colonnes enregistrées :

| Colonne | Description |
|---|---|
| prediction_id | identifiant unique de la prédiction |
| predicted_at | date et heure de prédiction |
| comment_text | commentaire analysé |
| predicted_intent | intention prédite |
| confidence_score | score de confiance |
| model_name | nom du modèle |
| model_version | version du modèle |
| response_time_ms | temps de réponse |
| is_low_confidence | indique si la prédiction est incertaine |
| low_confidence_threshold | seuil de faible confiance |
| source | origine de la prédiction |

## 6. Seuil de faible confiance

Le seuil retenu est :

```text
0.60
```

Si une prédiction a un score inférieur à ce seuil, elle est considérée comme faible en confiance.

Cela permet d'identifier les commentaires à revoir manuellement ou à utiliser pour améliorer le modèle.

## 7. Intégration avec l'API

Le monitoring est intégré dans :

```text
api/ai_service.py
```

Lorsqu'une prédiction est faite via l'API, elle est automatiquement enregistrée.

Fonctions utilisées :

```text
log_prediction()
log_batch_predictions()
```

Sources possibles :

```text
api_single
api_batch
```

Les endpoints de consultation du monitoring sont :

```text
GET /api/v1/ai/monitoring/dashboard
GET /api/v1/ai/monitoring/alerts
```

Ils sont protégés par la clé API comme les autres routes IA sensibles.

## 8. Rapport de monitoring

Le rapport est généré dans :

```text
data/ai/reports/model_monitoring_report.csv
```

Il contient plusieurs sections :

| Section | Description |
|---|---|
| global_summary | statistiques générales |
| predicted_intent_distribution | répartition des intentions |
| model_version_distribution | versions de modèles utilisées |
| prediction_source_distribution | origine des prédictions |
| low_confidence_examples | exemples de prédictions incertaines |

## 9. Métriques suivies

Les métriques suivies sont :

- nombre total de prédictions ;
- score moyen de confiance ;
- score minimum ;
- score maximum ;
- nombre de prédictions faibles en confiance ;
- pourcentage de prédictions faibles en confiance ;
- temps moyen de réponse ;
- temps maximum de réponse ;
- nombre de prédictions par intention ;
- nombre de prédictions par version de modèle ;
- nombre de prédictions par source.

## 10. Alertes de monitoring

Les alertes principales sont :

```text
LOW_CONFIDENCE
SLOW_RESPONSE
UNKNOWN_INTENT
```

Seuils utilisés :

```text
confidence_score < 0.60 → LOW_CONFIDENCE
response_time_ms > 1000 ms → SLOW_RESPONSE
predicted_intent = unknown → UNKNOWN_INTENT
```

Les alertes sont enregistrées dans :

```text
data/ai/reports/model_monitoring_alerts.csv
```

L'absence d'alerte est un résultat valide lorsqu'aucune prédiction ne franchit les seuils définis.

## 11. Génération du rapport et du dashboard

Rapport et alertes :

```cmd
python src\ai\monitoring\monitor_predictions.py
```

Dashboard HTML :

```cmd
python src\ai\monitoring\generate_monitoring_dashboard.py
```

Ces commandes permettent de recalculer les métriques et de générer une restitution actualisée à partir du journal de prédictions.

## 12. Test via API

Exemple d'appel API générant une ligne de log :

```powershell
$headers = @{ "X-API-Key" = "paylive-dev-api-key" }

$body = @{
    comment_text = "je prends la robe noire en M"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/ai/predict-intent" `
  -Method POST `
  -Headers $headers `
  -Body $body `
  -ContentType "application/json"
```

Après cet appel, le fichier suivant doit être présent ou mis à jour :

```text
data/ai/predictions/ai_predictions_log.csv
```

## 13. Vérification des fichiers

```cmd
dir data\ai\predictions
dir data\ai\reports
```

Fichiers attendus :

```text
ai_predictions_log.csv
model_monitoring_report.csv
model_monitoring_dashboard.html
model_monitoring_alerts.csv
```

Le dashboard peut aussi être consulté via :

```text
GET /api/v1/ai/monitoring/dashboard
```

et les alertes via :

```text
GET /api/v1/ai/monitoring/alerts
```

## 14. Problème rencontré et résolution

Pendant l'intégration, le service API Docker a rencontré une erreur d'import :

```text
ImportError: cannot import name 'log_prediction'
```

Analyse :

- l'API importait la fonction `log_prediction` ;
- le conteneur avait rechargé l'application pendant une modification ;
- il fallait vérifier que les fonctions existaient bien dans `monitor_predictions.py`.

Vérification réalisée :

```cmd
findstr /N /C:"def log_prediction" /C:"def log_batch_predictions" src\ai\monitoring\monitor_predictions.py
```

La reconstruction ou le redémarrage du conteneur API a permis de corriger l'erreur.

## 15. Intérêt métier du monitoring

Le monitoring permet à terme de répondre à des questions comme :

- combien de commentaires ont été analysés ?
- quelles intentions sont les plus fréquentes ?
- le modèle prédit-il trop souvent une classe ?
- combien de prédictions sont incertaines ?
- quels commentaires doivent être revus ?
- quelle version du modèle est utilisée ?
- certaines prédictions dépassent-elles les seuils de confiance ou de latence définis ?

Même si le projet est une preuve de concept, ce monitoring prépare une logique MLOps simple et contrôlable.

## 16. Limites du monitoring

Limites actuelles :

- stockage principal des prédictions et rapports sous forme de fichiers CSV locaux ;
- dashboard HTML local plutôt qu'une plateforme de monitoring centralisée ;
- pas de détection statistique automatique de dérive des données ;
- pas de réentraînement automatique ;
- pas de base dédiée aux logs IA ;
- alertes basées sur des seuils simples plutôt que sur un système distribué temps réel ;
- actualisation du dashboard déclenchée par les scripts de monitoring dans le POC.

Ces limites sont acceptables pour une preuve de concept. Elles permettent de distinguer clairement le fonctionnement actuel d'une future architecture de production.

## 17. Évolutions possibles

Évolutions envisagées :

- stockage des prédictions et alertes en base PostgreSQL ;
- dashboard dynamique connecté à une source de données centralisée ;
- suivi du drift de données et de concept ;
- métriques par période, version de modèle et source ;
- alerting temps réel ;
- réentraînement contrôlé à partir de corrections humaines ;
- automatisation de la régénération du dashboard ;
- intégration à une plateforme MLOps ou d'observabilité en contexte de production.

# 18. Validation du monitoring en environnement de test

## 18.1. Objectif de la validation

La chaîne de monitoring est validée dans un environnement de test contrôlé avec des données simulées. Cette validation vérifie que de nouvelles prédictions sont journalisées, que les métriques peuvent être recalculées, que le dashboard peut être régénéré et que les alertes peuvent être réévaluées.

Aucune donnée personnelle réelle n'est utilisée pour ce test.

## 18.2. Environnement de test

Services nécessaires :

```text
paylive_postgres
paylive_api
paylive_frontend
```

Démarrage :

```cmd
docker compose up -d postgres api frontend
docker compose ps
```

Frontend :

```text
http://127.0.0.1:8080
```

API :

```text
http://127.0.0.1:8000
```

## 18.3. État initial et capture avant test

Avant l'injection de nouvelles prédictions :

```cmd
dir data\ai\predictions
dir data\ai\reports
```

Puis :

```cmd
python src\ai\monitoring\monitor_predictions.py
python src\ai\monitoring\generate_monitoring_dashboard.py
```

Cette première génération constitue l'état **AVANT TEST**.

Une capture d'écran du dashboard est conservée sous un nom explicite :

```text
preuve_c11_monitoring_avant_test.png
```

La capture doit montrer les principales métriques disponibles avant l'ajout des nouvelles prédictions.

## 18.4. Test avec 10 prédictions simulées

Le test utilise dix commentaires fictifs couvrant plusieurs intentions :

| N° | Commentaire simulé |
|---:|---|
| 1 | je prends la robe noire en M |
| 2 | combien coûte le pull rouge |
| 3 | est-ce que vous livrez en Belgique |
| 4 | je peux payer par carte |
| 5 | je veux deux chemises bleues |
| 6 | quelle taille est encore disponible |
| 7 | je prends celui-ci |
| 8 | combien de jours pour la livraison |
| 9 | le paiement fonctionne avec paypal |
| 10 | merci pour le live |

Exemple d'appel :

```cmd
curl -X POST http://127.0.0.1:8000/api/v1/ai/predict-intent -H "Content-Type: application/json" -H "X-API-Key: paylive-dev-api-key" -d "{\"comment_text\":\"je prends la robe noire en M\"}"
```

Le même principe est appliqué aux dix commentaires. Chaque réponse doit retourner notamment :

```text
predicted_intent
confidence_score
response_time_ms
model_version
```

## 18.5. Génération du dashboard à chaque consultation ou actualisation

Dans l'environnement de test, **chaque cycle de consultation ou d'actualisation du monitoring est précédé d'une régénération du rapport, des alertes et du dashboard**.

Séquence :

```text
nouvelles prédictions
        ↓
monitor_predictions.py
        ↓
model_monitoring_report.csv
model_monitoring_alerts.csv
        ↓
generate_monitoring_dashboard.py
        ↓
model_monitoring_dashboard.html
        ↓
consultation via API / frontend
```

Commandes :

```cmd
python src\ai\monitoring\monitor_predictions.py
python src\ai\monitoring\generate_monitoring_dashboard.py
```

Dans le POC actuel, cette régénération est déclenchée par les scripts. Une version de production pourrait automatiser ce déclenchement via une tâche planifiée, une pipeline MLOps ou un service dédié.

## 18.6. Consultation du dashboard actualisé

Depuis le frontend :

```text
http://127.0.0.1:8080
```

ou directement depuis l'API :

```cmd
curl -H "X-API-Key: paylive-dev-api-key" -o dashboard_apres_test.html http://127.0.0.1:8000/api/v1/ai/monitoring/dashboard
start dashboard_apres_test.html
```

## 18.7. Capture après test et comparaison avant / après

Après les dix prédictions, le recalcul du monitoring et la régénération du dashboard, une seconde capture est réalisée :

```text
preuve_c11_monitoring_apres_test.png
```

La comparaison doit permettre d'observer :

- l'évolution du nombre de prédictions ;
- la distribution des intentions ;
- les scores de confiance ;
- les temps de réponse ;
- les alertes ;
- les prédictions éventuellement considérées comme faibles en confiance.

Tableau de vérification :

| Élément | Avant test | Après 10 prédictions | Résultat |
|---|---|---|---|
| journal de prédictions | état initial | +10 prédictions attendues | à renseigner |
| rapport de monitoring | généré | régénéré | à renseigner |
| dashboard HTML | disponible | actualisé | à renseigner |
| distribution des intentions | état initial | nouvelles valeurs intégrées | à renseigner |
| scores de confiance | état initial | nouvelles valeurs intégrées | à renseigner |
| temps de réponse | état initial | nouvelles valeurs intégrées | à renseigner |
| alertes | état initial | recalculées | à renseigner |

Les valeurs exactes sont relevées lors du test réel et ne doivent pas être inventées.

## 18.8. Tableau accessible en complément des graphiques

Les graphiques du dashboard sont complétés par une restitution tabulaire afin que les informations essentielles restent accessibles sous forme textuelle.

Exemple :

| Métrique | Valeur |
|---|---:|
| Nombre total de prédictions | valeur calculée |
| Score moyen de confiance | valeur calculée |
| Temps moyen de réponse | valeur calculée |
| Nombre de faibles confiances | valeur calculée |
| Nombre d'alertes | valeur calculée |

Distribution des intentions :

| Intention | Nombre de prédictions |
|---|---:|
| purchase_intent | valeur calculée |
| product_question | valeur calculée |
| payment_question | valeur calculée |
| shipping_question | valeur calculée |
| other | valeur calculée |
| unknown | valeur calculée |

Règles d'accessibilité :

- en-têtes de colonnes explicites ;
- ordre logique de lecture ;
- valeurs disponibles sous forme de texte ;
- aucune information transmise uniquement par couleur ;
- unités indiquées lorsque nécessaire ;
- graphiques utilisés comme complément et non comme seule source d'information.

## 18.9. Validation des alertes

Vérification du fichier :

```text
data/ai/reports/model_monitoring_alerts.csv
```

ou de l'endpoint :

```cmd
curl -H "X-API-Key: paylive-dev-api-key" http://127.0.0.1:8000/api/v1/ai/monitoring/alerts
```

Les alertes doivent être cohérentes avec les seuils définis dans la section 10.

## 18.10. Procédure d'installation

Pré-requis :

- Python ;
- environnement virtuel ;
- dépendances installées ;
- modèle IA entraîné ;
- API fonctionnelle.

Activation :

```cmd
.venv\Scripts\activate
```

Installation :

```cmd
pip install -r requirements.txt
```

Démarrage des services :

```cmd
docker compose up -d postgres api frontend
docker compose ps
```

Génération du monitoring :

```cmd
python src\ai\monitoring\monitor_predictions.py
python src\ai\monitoring\generate_monitoring_dashboard.py
```

Vérification :

```cmd
dir data\ai\reports
```

Fichiers attendus :

```text
model_monitoring_report.csv
model_monitoring_dashboard.html
model_monitoring_alerts.csv
```

## 18.11. Procédure d'utilisation

Pour chaque nouvelle validation :

1. vérifier que l'API est disponible ;
2. réaliser les prédictions de test ;
3. contrôler `ai_predictions_log.csv` ;
4. exécuter `monitor_predictions.py` ;
5. exécuter `generate_monitoring_dashboard.py` ;
6. consulter le dashboard ;
7. consulter le tableau des métriques ;
8. contrôler les alertes ;
9. comparer l'état avant / après ;
10. conserver les preuves.

## 18.12. Critères de réussite

La validation est considérée comme réussie lorsque :

- les dix prédictions sont exécutées sans erreur ;
- les nouvelles prédictions sont enregistrées ;
- le rapport peut être recalculé ;
- le dashboard peut être régénéré ;
- le dashboard actualisé est consultable ;
- les métriques reflètent les nouvelles prédictions ;
- les alertes respectent les seuils documentés ;
- les informations essentielles sont également disponibles dans un tableau textuel ;
- les captures avant et après permettent de démontrer l'évolution du monitoring.

## 18.13. Résultat du test à compléter après exécution

```text
Date du test :
Environnement :
Nombre de prédictions avant :
Nombre de prédictions injectées : 10
Nombre de prédictions après :
Nombre d'alertes avant :
Nombre d'alertes après :
Dashboard régénéré : OUI / NON
Tableau accessible vérifié : OUI / NON
Résultat global : VALIDÉ / À CORRIGER
```

Les valeurs sont renseignées uniquement après l'exécution réelle du test.

## 19. Captures d'écran et preuves recommandées

```text
preuve_c11_monitoring_avant_test.png
preuve_c11_10_predictions.png
preuve_c11_generation_dashboard.png
preuve_c11_monitoring_apres_test.png
preuve_c11_tableau_accessible.png
preuve_c11_alertes.png
```

À conserver également :

```text
[CAPTURE À AJOUTER]
Dossier data/ai/predictions avec ai_predictions_log.csv
```

```text
[CAPTURE À AJOUTER]
Dossier data/ai/reports avec le rapport, le dashboard et les alertes
```

```text
[CAPTURE À AJOUTER]
Extrait du fichier ai_predictions_log.csv
```

```text
[CAPTURE À AJOUTER]
Extrait du fichier model_monitoring_report.csv
```

## 20. Conclusion

Le monitoring IA assure la traçabilité des prédictions, le calcul de métriques, l'identification des faibles confiances et la génération d'alertes.

La chaîne est complétée par un dashboard HTML et par une validation en environnement de test avec des prédictions simulées. Cette validation permet de vérifier qu'après l'arrivée de nouvelles prédictions, les rapports et le dashboard peuvent être régénérés et que les informations importantes restent accessibles sous forme tabulaire en complément des graphiques.

Cette approche constitue une supervision adaptée au POC et prépare une évolution vers une architecture MLOps plus automatisée en contexte de production.
