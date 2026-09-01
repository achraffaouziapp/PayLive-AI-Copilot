#  Méthodologie agile du projet

## 1. Contexte du projet

Le projet a été réalisé dans le cadre d’un travail individuel, avec un suivi assuré par un encadrant pédagogique.

L’organisation retenue s’inspire de Scrum, mais elle a été adaptée à cette configuration particulière. Il n’existe pas dans le projet une équipe Scrum complète avec plusieurs développeurs, un Scrum Master dédié et un Product Owner distinct. Les différentes responsabilités ont été regroupées autour du porteur du projet, tandis que l’encadrant pédagogique intervient comme regard externe lors des points de suivi et de validation.

Cette adaptation permet de conserver les principes utiles de l’agilité :

- travail par cycles courts ;
- priorisation continue ;
- gestion d’un backlog ;
- réalisation incrémentale ;
- validation régulière ;
- amélioration continue ;
- traçabilité des tâches et décisions.

## 2. Méthode retenue

La méthode utilisée est :

```text
Scrum adaptée à un projet individuel
```

La durée retenue pour un cycle de travail est :

```text
1 sprint = 1 semaine
```

L’outil principal de gestion des tâches et du backlog est :

```text
Jira
```

Les outils complémentaires sont :

```text
Git
GitHub
VS Code
GitHub Actions
Docker
```

Jira est utilisé pour organiser et suivre le travail, tandis que Git et GitHub assurent la traçabilité technique des modifications du code source.

## 3. Organisation générale des cycles

Le projet est structuré sous forme de cycles courts d’une semaine.

Chaque cycle suit la logique suivante :

```text
Backlog Jira
    ↓
Sélection des tâches du sprint
    ↓
Sprint Planning
    ↓
Développement
    ↓
Tests et validation
    ↓
Mise à jour Jira
    ↓
Sprint Review
    ↓
Rétrospective
    ↓
Préparation du sprint suivant
```

L’objectif est de ne pas développer l’ensemble de l’application en une seule phase, mais de construire progressivement des fonctionnalités vérifiables.

## 4. Étapes d’un cycle

### 4.1. Préparation du backlog

Avant le démarrage d’un sprint, les besoins à traiter sont identifiés et enregistrés dans Jira.

Le backlog peut contenir :

- user stories ;
- tâches techniques ;
- bugs ;
- tâches de tests ;
- tâches de documentation ;
- améliorations ;
- travaux de déploiement ;
- corrections issues des retours de l’encadrant.

Chaque élément doit être suffisamment clair pour permettre de comprendre :

- ce qui doit être réalisé ;
- pourquoi la tâche est nécessaire ;
- sa priorité ;
- son état d’avancement.

### 4.2. Sélection des tâches

Au début de chaque sprint, les tâches prioritaires sont sélectionnées à partir du backlog Jira.

La sélection prend en compte :

- la priorité métier ;
- les dépendances techniques ;
- les éléments nécessaires au dossier professionnel ;
- les anomalies bloquantes ;
- les retours de l’encadrant ;
- la charge réalisable pendant la semaine.

L’objectif n’est pas d’intégrer le maximum de tickets possible, mais de sélectionner un ensemble cohérent et réalisable.

### 4.3. Développement

Les tâches sélectionnées sont réalisées progressivement.

Selon le sprint, cela peut concerner :

- développement frontend ;
- développement API ;
- intégration du modèle IA ;
- sécurité ;
- monitoring ;
- tests automatisés ;
- accessibilité ;
- Docker ;
- CI/CD ;
- documentation ;
- environnement de pré-production.

Le statut des tickets Jira est mis à jour afin de suivre l’avancement.

### 4.4. Tests

Une fonctionnalité n’est pas considérée comme terminée uniquement parce que son code a été écrit.

Elle doit être vérifiée à l’aide des moyens adaptés :

```text
tests unitaires
tests d’intégration
tests API
tests E2E
tests manuels
smoke tests
```

Les tests sont exécutés avant de considérer la tâche comme terminée.

Les anomalies détectées sont corrigées ou enregistrées dans Jira lorsqu’elles nécessitent un traitement ultérieur.

### 4.5. Validation

À la fin du cycle, les tâches terminées sont relues et vérifiées.

La validation porte notamment sur :

- conformité au besoin ;
- fonctionnement technique ;
- résultats des tests ;
- documentation ;
- intégration avec les autres composants ;
- absence de régression connue.

Lorsqu’un point de suivi avec l’encadrant est organisé, les fonctionnalités réalisées peuvent être présentées afin d’obtenir un retour externe.

### 4.6. Clôture du sprint

À la fin de la semaine :

- les tâches terminées sont clôturées dans Jira ;
- les tâches incomplètes sont réévaluées ;
- les problèmes rencontrés sont identifiés ;
- les priorités du prochain sprint sont ajustées ;
- les éventuels retours de l’encadrant sont intégrés au backlog.

## 5. Rôles et responsabilités

Le projet étant individuel, plusieurs responsabilités habituellement réparties dans une équipe Scrum sont regroupées.

| Rôle | Personne / acteur | Responsabilités |
|---|---|---|
| Porteur du projet | Étudiant | réalisation globale du projet |
| Product Owner adapté | Étudiant | priorisation du backlog, définition des objectifs du sprint |
| Développeur IA / full-stack | Étudiant | conception, développement, intégration, tests et documentation |
| Pilotage agile | Étudiant | suivi de Jira, organisation des cycles, gestion des priorités |
| Encadrant pédagogique | Encadrant | suivi, retours, validation des grandes orientations et accompagnement |

Il n’y a donc pas de Scrum Master dédié dans cette organisation.

La fonction de coordination est assurée directement par le porteur du projet, ce qui est cohérent avec le caractère individuel du travail.

## 6. Rituels

Les rituels Scrum classiques sont conservés sous une forme adaptée.

| Rituel | Fréquence | Participants | Objectif |
|---|---|---|---|
| Sprint Planning | lundi / début de sprint | étudiant | sélectionner et prioriser les tâches du sprint |
| Point d’avancement | chaque jour de développement | étudiant | vérifier l’avancement, les blocages et les priorités |
| Sprint Review | vendredi / fin de sprint | étudiant, avec encadrant lorsque prévu | vérifier ce qui a été réalisé et présenter les résultats |
| Rétrospective | fin de sprint | étudiant | analyser le déroulement du sprint et améliorer le suivant |

## 7. Sprint Planning

Le Sprint Planning est réalisé au début de chaque semaine.

### Objectifs

- consulter le backlog Jira ;
- sélectionner les tâches les plus importantes ;
- définir un objectif de sprint ;
- vérifier les dépendances ;
- répartir le travail sur la semaine ;
- éviter de surcharger le sprint.

Exemple d’objectif :

```text
Objectif du sprint :
finaliser l’intégration frontend/API et sécuriser
les tests de communication avec le service IA.
```

Le Sprint Planning permet donc de commencer la semaine avec un périmètre clair.

## 8. Point d’avancement

Le projet ne disposant pas d’une équipe quotidienne, le Daily Scrum classique est remplacé par un point d’avancement personnel effectué chaque jour de développement.

Les questions utilisées sont :

```text
Qu’est-ce qui a été terminé ?
Qu’est-ce qui doit être fait ensuite ?
Existe-t-il un blocage ?
Une priorité doit-elle être modifiée ?
```

### Objectifs

- suivre régulièrement l’avancement ;
- détecter rapidement les blocages ;
- mettre à jour Jira ;
- ajuster la priorité des tâches si nécessaire ;
- éviter d’attendre la fin de semaine pour identifier un problème.

Ce point peut rester très court.

## 9. Sprint Review

La Sprint Review est réalisée à la fin du sprint.

### Objectifs

- vérifier les tâches réellement terminées ;
- contrôler les résultats ;
- comparer le résultat avec l’objectif initial ;
- identifier les fonctionnalités encore incomplètes ;
- présenter les avancées à l’encadrant lorsqu’un point de suivi est prévu ;
- récupérer de nouveaux retours.

Les éléments vérifiés peuvent comprendre :

```text
fonctionnalités réalisées
tests réussis
captures
documentation
tickets Jira
commits Git
workflow CI
déploiement
```

La Sprint Review permet donc de vérifier concrètement ce qui est utilisable à la fin du cycle.

## 10. Rétrospective

La rétrospective est réalisée après la revue de fin de sprint.

Elle porte sur trois questions principales :

```text
Qu’est-ce qui a bien fonctionné ?
Qu’est-ce qui a posé problème ?
Que faut-il améliorer au prochain sprint ?
```

### Objectifs

- capitaliser sur les pratiques efficaces ;
- identifier les difficultés ;
- améliorer l’organisation personnelle ;
- modifier la planification si nécessaire ;
- éviter de répéter les mêmes erreurs.

Exemples d’améliorations possibles :

- découper davantage les tickets trop importants ;
- lancer les tests plus tôt ;
- documenter une fonctionnalité dès sa validation ;
- vérifier les dépendances Docker avant la fin du sprint ;
- ajouter un ticket spécifique pour les preuves du dossier professionnel.

## 11. Gestion du backlog avec Jira

Jira constitue l’outil principal de pilotage du projet.

Le backlog regroupe les tâches à réaliser.

Les éléments peuvent être classés selon plusieurs catégories :

```text
User Story
Tâche
Bug
Amélioration
Documentation
Test
Déploiement
```

Pour chaque ticket, les informations utiles sont :

```text
titre
description
priorité
critères d’acceptation
statut
résultat
preuve éventuelle
```

Exemple :

```text
Titre :
Ajouter les tests E2E du frontend IA

Description :
Vérifier que le frontend communique réellement
avec les endpoints IA exploités.

Critères d’acceptation :
- connexion API testée ;
- prédiction testée ;
- model-info testé ;
- métriques testées ;
- monitoring testé.

Statut :
Terminé
```

## 12. Statuts Jira

Les statuts utilisés servent à visualiser l’état du travail.

Exemple de cycle :

```text
À faire
↓
En cours
↓
À tester / À valider
↓
Terminé
```

Une tâche bloquée peut également être identifiée explicitement afin de ne pas la confondre avec une tâche simplement en cours.

L’objectif est d’obtenir une vision immédiate du travail restant et des éléments terminés.

## 13. Priorisation du backlog

Les tâches ne sont pas traitées uniquement dans leur ordre de création.

La priorité prend en compte :

1. les fonctionnalités essentielles ;
2. les dépendances techniques ;
3. les anomalies bloquantes ;
4. les critères de validation du projet ;
5. les retours de l’encadrant ;
6. les améliorations non bloquantes.

Exemple :

```text
Critique :
API inaccessible

Haute :
prédiction frontend non fonctionnelle

Moyenne :
amélioration de la documentation

Basse :
amélioration esthétique non bloquante
```

Cette organisation permet de concentrer les efforts sur les éléments les plus importants.

## 14. Collaboration avec l’encadrant

Même si le développement est individuel, le projet ne se déroule pas sans suivi externe.

L’encadrant pédagogique intervient notamment pour :

- suivre l’avancement ;
- apporter un regard extérieur ;
- signaler des axes d’amélioration ;
- vérifier la cohérence du projet ;
- aider à valider les grandes orientations ;
- contrôler l’adéquation avec les attendus pédagogiques.

Les retours issus de ces échanges peuvent conduire à :

```text
création d’un nouveau ticket Jira
modification d’une priorité
correction d’une fonctionnalité
amélioration de la documentation
ajout d’un test
```

La collaboration est donc principalement une collaboration de suivi, de conseil et de validation.

## 15. Outils de collaboration et de traçabilité

### Jira

Utilisé pour :

- backlog ;
- tickets ;
- priorités ;
- suivi d’avancement ;
- anomalies ;
- tâches de documentation ;
- validation des fonctionnalités.

### Git

Utilisé pour :

- versionner le code ;
- identifier les changements ;
- conserver l’historique.

### GitHub

Utilisé pour :

- héberger le dépôt ;
- centraliser les versions ;
- exécuter GitHub Actions ;
- publier les artefacts techniques ;
- conserver les preuves de CI/CD.

### GitHub Actions

Utilisé pour automatiser :

- préparation des données ;
- entraînement ;
- tests ;
- validation ;
- packaging ;
- publication de l’image Docker.

## 16. Exemple de sprint projet

### Objectif du sprint

```text
Finaliser l’intégration de l’application web avec le service IA.
```

### Backlog sélectionné

| Ticket | Type | Priorité | Résultat attendu |
|---|---|---|---|
| Interface de prédiction | User Story | Haute | commentaire analysable depuis le frontend |
| Authentification API | Tâche | Haute | clé API transmise correctement |
| Informations modèle | User Story | Moyenne | model-info consultable |
| Métriques modèle | User Story | Moyenne | métriques affichées |
| Tests frontend | Test | Haute | communication frontend/API validée |
| Accessibilité | Amélioration | Moyenne | critères WCAG/RGAA intégrés |

### Cycle

```text
Lundi
→ Sprint Planning

Mardi
→ développement interface et API

Mercredi
→ intégration modèle et corrections

Jeudi
→ tests automatisés et tests E2E

Vendredi
→ revue, documentation et rétrospective
```

## 17. Exemple de sprint de préparation pré-production

### Objectif

```text
Rendre la preuve de concept accessible
dans un environnement de pré-production.
```

Tickets possibles :

```text
Configurer CORS
Ajouter tests CORS
Construire image API + modèle
Publier l’image dans GHCR
Créer environnement Render
Déployer API
Déployer frontend
Exécuter smoke tests
Documenter la validation pré-production
```

Ce découpage permet de suivre précisément la progression jusqu’à la mise à disposition de la preuve de concept.

## 18. Gestion des anomalies

Lorsqu’une anomalie est détectée, elle est :

1. reproduite ;
2. analysée ;
3. enregistrée dans Jira si nécessaire ;
4. priorisée ;
5. corrigée ;
6. retestée ;
7. clôturée après validation.

Exemples d’anomalies rencontrées dans le projet :

- problème de communication frontend/API ;
- configuration d’authentification ;
- problème Docker ;
- comportement incorrect d’une route ;
- problème de monitoring ;
- problème de CORS en préparation de la pré-production.

Cette procédure évite de considérer une anomalie comme corrigée sans vérification.

## 19. Définition d’une tâche terminée

Une tâche n’est considérée comme terminée que lorsque les éléments pertinents sont satisfaits.

Exemple de Definition of Done adaptée :

```text
fonctionnalité réalisée
code versionné
tests exécutés
résultat attendu obtenu
anomalies bloquantes corrigées
documentation mise à jour si nécessaire
ticket Jira mis à jour
preuve conservée si nécessaire
```

Cette règle permet d’éviter de clôturer une tâche alors que sa validation n’est pas terminée.

## 20. Adaptation au caractère individuel du projet

L’utilisation de Scrum dans ce projet constitue une adaptation et non une application stricte de Scrum en équipe.

Certaines limites existent :

- absence d’équipe de développement ;
- absence de Scrum Master dédié ;
- Product Owner et développeur représentés par la même personne ;
- point quotidien personnel plutôt qu’une réunion d’équipe ;
- Sprint Review réalisée principalement comme auto-validation, complétée par les retours de l’encadrant lorsqu’ils sont disponibles.

Cette adaptation reste utile car elle conserve les principes essentiels :

```text
cycles courts
priorisation
backlog
rituels
contrôle régulier
amélioration continue
traçabilité
```

Le document ne cherche donc pas à simuler artificiellement une équipe inexistante.

## 21. Preuves à conserver

Pour démontrer l’organisation agile, les preuves suivantes peuvent être conservées :

```text
capture_jira_backlog.png
capture_jira_sprint.png
capture_jira_ticket_user_story.png
capture_jira_ticket_bug.png
capture_jira_ticket_termine.png
capture_historique_git.png
capture_github_actions.png
```

Captures particulièrement utiles :

1. backlog Jira avec plusieurs tickets ;
2. tickets avec statuts différents ;
3. ticket contenant des critères d’acceptation ;
4. ticket clôturé après validation ;
5. historique Git correspondant à une fonctionnalité ;
6. preuve d’un retour ou d’une validation de l’encadrant si disponible.

## 22. Synthèse C16

| Élément | Mise en œuvre |
|---|---|
| Méthode | Scrum adaptée à un projet individuel |
| Cycle | sprint d’une semaine |
| Étapes | planification, développement, tests, validation, revue, rétrospective |
| Rôles | porteur du projet, Product Owner adapté, développeur IA/full-stack, encadrant pédagogique |
| Rituels | Sprint Planning, point d’avancement, Sprint Review, rétrospective |
| Outil de pilotage | Jira |
| Backlog | user stories, tâches, bugs, tests, documentation, déploiement |
| Collaboration | suivi et validation avec l’encadrant |
| Traçabilité technique | Git / GitHub |
| Objectif des rituels | planifier, suivre, valider et améliorer |

## 23. Conclusion

Le projet est réalisé individuellement, mais son organisation repose sur une démarche agile structurée inspirée de Scrum.

Les développements sont organisés en sprints d’une semaine, avec un backlog géré dans Jira, une planification en début de cycle, un suivi régulier, une revue des résultats et une rétrospective.

Les responsabilités de Product Owner, de développeur et de pilotage sont assumées par le porteur du projet. L’encadrant pédagogique apporte un suivi externe et intervient pour donner des retours et valider les grandes orientations.

Cette organisation permet de conserver les bénéfices d’un fonctionnement agile tout en restant cohérente avec la réalité d’un projet individuel.
