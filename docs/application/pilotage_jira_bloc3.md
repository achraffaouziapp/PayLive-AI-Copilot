# Pilotage du développement avec Jira — Bloc 3 PayLive AI Copilot

## 1. Objectif du document

Ce document présente l’organisation du suivi de développement du Bloc 3 avec **Jira**.

Le Bloc 3 consiste à développer une application web HTML/CSS/JavaScript conteneurisée avec Docker/Nginx, connectée à l’API IA FastAPI créée dans le Bloc 2.

L’objectif du suivi Jira est de :

- découper le développement en tâches suivables ;
- prioriser les fonctionnalités ;
- suivre l’avancement ;
- documenter les bugs et corrections ;
- conserver une preuve de pilotage projet ;
- relier les tâches aux livrables du dossier professionnel.

## 2. Outil de suivi retenu

L’outil retenu pour le suivi du développement est :

```text
Jira
```

Jira est utilisé comme outil central pour gérer :

- le backlog ;
- les user stories ;
- les tâches techniques ;
- les bugs ;
- les critères d’acceptation ;
- les statuts d’avancement ;
- les preuves associées aux développements.

Le projet n’utilise pas un outil externe séparé pour le suivi. Le pilotage est centralisé dans Jira.

## 3. Organisation Jira du Bloc 3

Le projet Jira est organisé autour du développement de l’application web du Bloc 3.

Exemple de nom de projet Jira :

```text
PayLive AI Copilot — Bloc 3 Application
```

Exemple de clé projet :

```text
PAYLIVE
```

Les tickets sont organisés par type :

| Type Jira | Utilisation dans le projet |
|---|---|
| Epic | Grand ensemble fonctionnel |
| Story | Besoin utilisateur exprimé sous forme de user story |
| Task | Tâche technique de développement ou configuration |
| Bug | Anomalie détectée pendant les tests |
| Documentation | Mise à jour des documents du dossier |
| Test | Validation fonctionnelle, technique ou accessibilité |

## 4. Workflow Jira utilisé

Le workflow Jira utilisé est volontairement simple.

| Statut Jira | Signification |
|---|---|
| À faire | Le ticket est identifié mais pas encore commencé |
| En cours | Le développement ou la rédaction est en cours |
| En revue | Le ticket est terminé et doit être vérifié |
| Terminé | Le ticket est validé et intégré au projet |

Ce workflow permet de suivre clairement l’avancement du Bloc 3 sans alourdir la gestion de projet.

## 5. Epics du Bloc 3

Les principaux Epics Jira du Bloc 3 sont les suivants :

| Epic | Objectif |
|---|---|
| EPIC-01 — Cadrage applicatif | Définir le besoin, les fonctionnalités et le périmètre |
| EPIC-02 — Architecture frontend | Concevoir l’architecture HTML/CSS/JS et Docker |
| EPIC-03 — Développement interface | Développer l’application web utilisateur |
| EPIC-04 — Intégration API IA | Connecter le frontend à l’API FastAPI |
| EPIC-05 — Monitoring et alertes | Accéder au dashboard IA et aux alertes |
| EPIC-06 — Tests et qualité | Tester l’application et automatiser les contrôles |
| EPIC-07 — Documentation Bloc 3 | Documenter la conception, les tests et le bilan |

## 6. Backlog Jira du Bloc 3

Le backlog initial du Bloc 3 contient les tickets suivants.

| ID Jira | Type | Titre | Priorité | Statut |
|---|---|---|---|---|
| PAYLIVE-31 | Story | En tant que vendeur, je veux saisir un commentaire de live afin d’obtenir une prédiction d’intention | Haute | Terminé |
| PAYLIVE-32 | Story | En tant que vendeur, je veux voir l’intention prédite et le score de confiance | Haute | Terminé |
| PAYLIVE-33 | Story | En tant que vendeur, je veux être averti si la confiance du modèle est faible | Moyenne | Terminé |
| PAYLIVE-34 | Story | En tant qu’administrateur, je veux tester la validité de la clé API | Haute | Terminé |
| PAYLIVE-35 | Story | En tant qu’administrateur, je veux consulter les informations du modèle IA | Moyenne | Terminé |
| PAYLIVE-36 | Story | En tant qu’administrateur, je veux consulter les métriques du modèle IA | Moyenne | Terminé |
| PAYLIVE-37 | Story | En tant qu’administrateur, je veux ouvrir le dashboard de monitoring IA depuis l’application | Moyenne | Terminé |
| PAYLIVE-38 | Story | En tant qu’administrateur, je veux télécharger les alertes de monitoring IA | Moyenne | Terminé |
| PAYLIVE-39 | Task | Créer la structure frontend HTML/CSS/JS | Haute | Terminé |
| PAYLIVE-40 | Task | Créer le Dockerfile frontend avec Nginx | Haute | Terminé |
| PAYLIVE-41 | Task | Configurer Nginx pour servir le frontend et proxifier l’API | Haute | Terminé |
| PAYLIVE-42 | Task | Ajouter le service frontend dans docker-compose.yml | Haute | Terminé |
| PAYLIVE-43 | Task | Ajouter les tests statiques frontend | Moyenne | Terminé |
| PAYLIVE-44 | Task | Ajouter le build Docker frontend dans GitHub Actions | Moyenne | Terminé |
| PAYLIVE-45 | Documentation | Mettre à jour la documentation de développement interface | Moyenne | Terminé |
| PAYLIVE-46 | Documentation | Mettre à jour la documentation de tests application | Moyenne | Terminé |
| PAYLIVE-47 | Bug | Corriger l’affichage des sections modèle et métriques | Moyenne | Terminé |
| PAYLIVE-48 | Bug | Corriger le test de clé API qui utilisait une route publique | Haute | Terminé |

## 7. User stories principales

## 7.1. Story — Saisie d’un commentaire

| Élément | Description |
|---|---|
| ID Jira | PAYLIVE-31 |
| User story | En tant que vendeur, je veux saisir un commentaire de live afin d’obtenir une prédiction d’intention. |
| Priorité | Haute |
| Critères d’acceptation | Le champ commentaire est visible ; le bouton d’analyse est visible ; un commentaire vide est refusé ; un commentaire valide déclenche un appel API. |
| Statut | Terminé |

## 7.2. Story — Affichage de la prédiction

| Élément | Description |
|---|---|
| ID Jira | PAYLIVE-32 |
| User story | En tant que vendeur, je veux voir l’intention prédite et le score de confiance afin de comprendre le résultat IA. |
| Priorité | Haute |
| Critères d’acceptation | L’intention prédite est affichée ; le score de confiance est affiché ; le temps de réponse est affiché ; la version du modèle est affichée. |
| Statut | Terminé |

## 7.3. Story — Validation de la clé API

| Élément | Description |
|---|---|
| ID Jira | PAYLIVE-34 |
| User story | En tant qu’administrateur, je veux tester la validité de la clé API afin de vérifier que l’application peut accéder aux routes protégées. |
| Priorité | Haute |
| Critères d’acceptation | Une clé valide affiche un message de succès ; une clé invalide affiche une erreur ; le test utilise une route protégée ; la route publique `/health` n’est pas utilisée comme validation de sécurité. |
| Statut | Terminé |

## 7.4. Story — Accès au monitoring IA

| Élément | Description |
|---|---|
| ID Jira | PAYLIVE-37 |
| User story | En tant qu’administrateur, je veux ouvrir le dashboard de monitoring IA depuis l’application afin de suivre l’état du service IA. |
| Priorité | Moyenne |
| Critères d’acceptation | Le bouton dashboard est visible ; l’appel API inclut la clé API ; le dashboard s’ouvre dans un nouvel onglet ; une erreur est affichée si l’accès échoue. |
| Statut | Terminé |

## 8. Critères d’acceptation globaux

Les critères d’acceptation globaux du Bloc 3 sont :

| Critère | Résultat attendu |
|---|---|
| Application accessible | Le frontend est disponible sur `http://127.0.0.1:8080` |
| API intégrée | Le frontend appelle les routes IA FastAPI |
| Authentification | Les routes protégées utilisent `X-API-Key` |
| Prédiction IA | Une intention et un score de confiance sont affichés |
| Gestion erreur | Une clé invalide déclenche un message d’erreur |
| Monitoring | Le dashboard IA est accessible depuis l’interface |
| Alertes | Le fichier CSV d’alertes est téléchargeable |
| Dockerisation | Le frontend est lancé dans le conteneur `paylive_frontend` |
| Tests | Les tests `tests/test_frontend_static.py` passent |
| CI | GitHub Actions exécute les tests et le build Docker frontend |

## 9. Definition of Ready

Un ticket est prêt à être développé si :

- le besoin est compréhensible ;
- le résultat attendu est défini ;
- les critères d’acceptation sont indiqués ;
- les dépendances techniques sont identifiées ;
- l’impact sur l’API, le frontend ou Docker est précisé ;
- le ticket est priorisé.

## 10. Definition of Done

Un ticket est terminé si :

- le code est développé ;
- le comportement est testé localement ;
- les erreurs connues sont corrigées ou documentées ;
- les tests automatisés passent ;
- la CI GitHub Actions passe en vert ;
- la documentation est mise à jour si nécessaire ;
- les fichiers sont commités dans Git.

## 11. Suivi des preuves Jira

Les preuves à conserver dans le dossier professionnel sont :

```text
capture du projet Jira
capture du backlog Jira
capture d’un ticket user story terminé
capture d’un ticket bug corrigé
capture d’un ticket documentation
capture du workflow Jira avec les statuts
capture GitHub Actions en vert
```

## 12. Correspondance Jira / livrables projet

| Ticket Jira | Livrable projet |
|---|---|
| PAYLIVE-39 | `frontend/index.html`, `frontend/css/styles.css`, `frontend/js/app.js` |
| PAYLIVE-40 | `frontend/Dockerfile` |
| PAYLIVE-41 | `frontend/nginx.conf` |
| PAYLIVE-42 | `docker-compose.yml` |
| PAYLIVE-43 | `tests/test_frontend_static.py` |
| PAYLIVE-44 | `.github/workflows/ai_mlops_ci.yml` |
| PAYLIVE-45 | `docs/08_application/35_developpement_interface.md` |
| PAYLIVE-46 | `docs/08_application/36_tests_application.md` |
| PAYLIVE-47 | correction CSS dans `frontend/css/styles.css` |
| PAYLIVE-48 | correction test API key dans `frontend/js/app.js` |

## 13. Conclusion

Le développement du Bloc 3 est piloté avec Jira.

L’utilisation de Jira permet de démontrer une organisation structurée du travail, avec des tickets, des priorités, des critères d’acceptation, des statuts d’avancement, des corrections de bugs et des preuves associées.

Ce suivi complète les preuves techniques du Bloc 3 : application Dockerisée, intégration API IA, tests automatisés et GitHub Actions en vert.
