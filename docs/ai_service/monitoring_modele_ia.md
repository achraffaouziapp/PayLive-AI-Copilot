# Monitoring du modèle IA — PayLive AI Copilot

## 1. Objectif du document

Ce document décrit le monitoring mis en place pour le modèle IA du projet **PayLive AI Copilot**.

Le monitoring permet de suivre les prédictions réalisées par le service IA et de produire des indicateurs utiles sur son fonctionnement.

## 2. Objectif du monitoring

Le monitoring répond à plusieurs objectifs :

- historiser les prédictions ;
- suivre le nombre de prédictions ;
- suivre les classes prédites ;
- suivre les scores de confiance ;
- identifier les prédictions incertaines ;
- suivre les temps de réponse ;
- suivre la version du modèle utilisée ;
- produire un rapport exploitable pour le dossier professionnel.

## 3. Fichier de monitoring

Le script principal est :

```text
src/ai/monitoring/monitor_predictions.py
```

Il permet :

- d’enregistrer une prédiction ;
- d’enregistrer un batch de prédictions ;
- de lire le log existant ;
- de générer un rapport de monitoring.

## 4. Fichiers générés

Le monitoring génère deux fichiers principaux :

```text
data/ai/predictions/ai_predictions_log.csv
data/ai/reports/model_monitoring_report.csv
```

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

Cela permet d’identifier les commentaires à revoir manuellement ou à utiliser pour améliorer le modèle.

## 7. Intégration avec l’API

Le monitoring est intégré dans :

```text
api/ai_service.py
```

Lorsqu’une prédiction est faite via l’API, elle est automatiquement enregistrée.

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

## 10. Commande de génération du rapport

```bash
python src/ai/monitoring/monitor_predictions.py
```

Cette commande lit le fichier de log et régénère le rapport de monitoring.

## 11. Test via API

Exemple d’appel API générant une ligne de log :

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

Après cet appel, le fichier suivant doit être présent :

```text
data/ai/predictions/ai_predictions_log.csv
```

## 12. Vérification des fichiers

```bash
dir data\ai\predictions
dir data\ai\reports
```

Fichiers attendus :

```text
ai_predictions_log.csv
model_monitoring_report.csv
```

## 13. Problème rencontré et résolution

Pendant l’intégration, le service API Docker a rencontré une erreur d’import :

```text
ImportError: cannot import name 'log_prediction'
```

Analyse :

- l’API importait la fonction `log_prediction` ;
- le conteneur avait rechargé l’application pendant une modification ;
- il fallait vérifier que les fonctions existaient bien dans `monitor_predictions.py`.

Vérification réalisée :

```bash
findstr /N /C:"def log_prediction" /C:"def log_batch_predictions" src\ai\monitoring\monitor_predictions.py
```

La reconstruction ou le redémarrage du conteneur API a permis de corriger l’erreur.

## 14. Intérêt métier du monitoring

Le monitoring permet à terme de répondre à des questions comme :

- combien de commentaires ont été analysés ?
- quelles intentions sont les plus fréquentes ?
- le modèle prédit-il trop souvent une classe ?
- combien de prédictions sont incertaines ?
- quels commentaires doivent être revus ?
- quelle version du modèle est utilisée ?

Même si le projet est une preuve de concept, ce monitoring prépare une logique MLOps simple.

## 15. Limites du monitoring

Limites actuelles :

- monitoring local en CSV ;
- pas de tableau de bord graphique ;
- pas de détection automatique de dérive ;
- pas de réentraînement automatique ;
- pas de base dédiée aux logs IA ;
- pas d’alerting en temps réel.

Ces limites sont acceptables pour une première version pédagogique.

## 16. Évolutions possibles

Évolutions envisagées :

- stockage des prédictions en base PostgreSQL ;
- tableau de bord de monitoring ;
- suivi du drift de données ;
- détection de baisse de confiance ;
- alertes en cas d’anomalie ;
- réentraînement à partir de corrections manuelles ;
- suivi des performances par version de modèle.

## 17. Emplacements pour captures d’écran

```text
[CAPTURE À AJOUTER]
Dossier data/ai/predictions avec ai_predictions_log.csv
```

```text
[CAPTURE À AJOUTER]
Dossier data/ai/reports avec model_monitoring_report.csv
```

```text
[CAPTURE À AJOUTER]
Extrait du fichier ai_predictions_log.csv
```

```text
[CAPTURE À AJOUTER]
Extrait du fichier model_monitoring_report.csv
```

## 18. Conclusion

Le monitoring IA permet de tracer les prédictions réalisées par le modèle et de produire des indicateurs de suivi.

Cette étape complète le service IA en ajoutant une couche de supervision indispensable pour un système d’intelligence artificielle exploitable.
