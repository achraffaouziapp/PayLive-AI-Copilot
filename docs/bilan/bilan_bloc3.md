# Bilan du Bloc 3 — Application intégrant un service IA

## 1. Objectif

Ce document présente le bilan du Bloc 3 du projet **PayLive AI Copilot**.

Le Bloc 3 avait pour objectif de développer une application intégrant le service IA construit au Bloc 2.

## 2. Réalisations principales

| Réalisation | Description |
|---|---|
| cadrage applicatif | besoin utilisateur et périmètre |
| spécifications fonctionnelles | fonctionnalités attendues |
| architecture frontend | HTML, CSS, JavaScript, Nginx, Docker |
| intégration API IA | appels vers FastAPI |
| sécurité | clé API `X-API-Key` |
| monitoring intégré | dashboard et alertes accessibles depuis le frontend |
| tests frontend | tests statiques avec Pytest |
| CI | tests frontend et build Docker dans GitHub Actions |

## 3. Application livrée

L’application est disponible à l’adresse :

```text
http://127.0.0.1:8080
```

Elle est exécutée dans le conteneur :

```text
paylive_frontend
```

Elle communique avec :

```text
paylive_api
```

## 4. Fonctionnalités livrées

L’application permet de :

- configurer l’URL API ;
- configurer la clé API ;
- tester une connexion sécurisée ;
- saisir un commentaire ;
- prédire une intention ;
- afficher un score de confiance ;
- afficher un avertissement de faible confiance ;
- afficher les informations du modèle ;
- afficher les métriques du modèle ;
- ouvrir le dashboard de monitoring ;
- télécharger les alertes CSV.

## 5. Architecture technique finale

```text
Navigateur utilisateur
  ↓
Frontend Nginx Docker
  ↓
API FastAPI Docker
  ↓
Modèle IA scikit-learn
  ↓
Fichiers monitoring
```

Services Docker :

```text
paylive_postgres
paylive_pgadmin
paylive_api
paylive_frontend
```

## 6. Routes API consommées

```text
GET  /api/v1/ai/model-info
GET  /api/v1/ai/model-metrics
POST /api/v1/ai/predict-intent
GET  /api/v1/ai/monitoring/dashboard
GET  /api/v1/ai/monitoring/alerts
```

## 7. Tests réalisés

Fichier :

```text
tests/test_frontend_static.py
```

Commande :

```bash
pytest tests/test_frontend_static.py -v
```

Résultat attendu :

```text
7 passed
```

Tests intégrés dans la CI :

```text
.github/workflows/ai_mlops_ci.yml
```

Le workflow GitHub Actions passe en vert.

## 8. Difficultés et corrections

| Difficulté | Correction |
|---|---|
| mauvaise clé API acceptée lors du test connexion | utilisation de `/model-info`, route protégée |
| sections trop serrées | passage de la grille CSS à une colonne |
| JSON trop large | ajout de `overflow`, `pre-wrap`, `word-break` |
| accès dashboard depuis le frontend | récupération HTML depuis l’API et ouverture dans un onglet |
| besoin d’intégration Docker | ajout d’un service `frontend` dans Docker Compose |

## 9. Accessibilité et ergonomie

Éléments mis en place :

- labels sur les champs ;
- boutons explicites ;
- messages de statut ;
- `aria-live` ;
- design responsive ;
- séparation des sections ;
- affichage JSON lisible ;
- message visible en cas de faible confiance.

## 10. Couverture des attendus

| Attendu | Couverture |
|---|---|
| application intégrant un service IA | frontend connecté à l’API IA |
| appel API | JavaScript `fetch` |
| authentification | `X-API-Key` |
| traitement de réponse | parsing JSON |
| affichage résultat | intention, confiance, temps, modèle |
| accessibilité | labels, responsive, messages |
| tests | Pytest frontend |
| conteneurisation | Docker/Nginx |
| CI | GitHub Actions vert |
| monitoring | dashboard et alertes accessibles |

## 11. Preuves à fournir

[INSÉRER CAPTURE — Application frontend]

[INSÉRER CAPTURE — Prédiction IA]

[INSÉRER CAPTURE — Clé API invalide]

[INSÉRER CAPTURE — Dashboard monitoring]

[INSÉRER CAPTURE — Alertes CSV]

[INSÉRER CAPTURE — Docker ps]

[INSÉRER CAPTURE — Tests Pytest]

[INSÉRER CAPTURE — GitHub Actions vert]

## 12. Limites

Limites actuelles :

- pas de framework frontend avancé ;
- pas d’authentification JWT ;
- pas de gestion multi-utilisateurs ;
- pas d’audit accessibilité complet ;
- pas de tests end-to-end navigateur ;
- pas de déploiement cloud.

## 13. Évolutions possibles

Évolutions futures :

- ajouter Playwright ou Cypress ;
- ajouter JWT ;
- ajouter un historique des prédictions ;
- ajouter un tableau de bord métier ;
- améliorer le design ;
- ajouter un audit Lighthouse ;
- déployer sur un environnement cloud.

## 14. Conclusion

Le Bloc 3 est fonctionnel, documenté, testé et intégré dans Docker et GitHub Actions.

Il démontre que le service IA du Bloc 2 peut être consommé par une application utilisateur simple et exploitable dans un contexte de live shopping.

Le projet dispose désormais d’une chaîne complète :

```text
données → modèle IA → API → monitoring → application frontend → CI
```
