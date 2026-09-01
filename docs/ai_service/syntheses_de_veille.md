# Synthèses de veille technique et réglementaire IA

## 1. Rôle de ce document

Ce document centralise les synthèses produites à partir des séances de veille réellement réalisées.

Chaque synthèse doit répondre à trois questions :

1. **Qu'est-ce qui a changé ou qu'ai-je appris ?**
2. **Quel impact cette information peut-elle avoir sur le projet ?**
3. **Quelle décision a été prise ?**

Le détail temporel des séances est conservé dans :

```text
docs/ai_service/23b_journal_de_veille.csv
```

---

## 2. Format d'une synthèse

Chaque nouvelle synthèse doit utiliser le modèle suivant.

### [Date] — [Sujet]

**Durée :** 1 h  
**Source principale :**  
**Sources de confirmation :**  
**Outil de collecte :** Feedly/RSS, newsletter officielle, GitHub Releases ou consultation officielle.

#### Résumé

Décrire en quelques paragraphes l'information importante, sans recopier la source.

#### Analyse pour le projet

Préciser :
- les composants concernés ;
- les avantages ;
- les risques ;
- les contraintes ;
- le caractère urgent ou non.

#### Décision projet

Choisir une décision explicite :
- `CONSERVER`
- `TESTER`
- `METTRE À JOUR`
- `DOCUMENTER`
- `SURVEILLER`
- `ÉCARTER`

Puis expliquer la justification.

#### Actions

- ticket Jira :
- fichier à modifier :
- test à lancer :
- responsable :
- échéance :

---

# 3. Synthèses thématiques déjà reliées au projet

Les sections suivantes reprennent les principaux axes qui ont déjà influencé les choix du projet. Les dates exactes et les séances correspondantes doivent être renseignées dans le journal à partir des preuves disponibles.

## 3.1. Classification NLP — modèle local

### Constat

Le besoin principal consiste à classifier des commentaires courts de live shopping selon plusieurs intentions. Pour ce type de tâche, une approche supervisée légère permet d'obtenir un modèle rapide à entraîner, facile à intégrer et interprétable.

### Impact sur le projet

Les critères importants sont :
- temps de réponse faible ;
- coût maîtrisé ;
- fonctionnement local ;
- absence d'envoi de commentaires à un fournisseur tiers ;
- intégration simple dans FastAPI ;
- possibilité de mesurer précisément accuracy et F1.

### Décision projet

**CONSERVER — TF-IDF + Logistic Regression pour le POC.**

La solution reste proportionnée au besoin actuel. Des modèles plus complexes pourront être testés si le périmètre évolue vers l'extraction d'entités, le multilingue ou des formulations plus difficiles.

---

## 3.2. Services IA externes

### Constat

Les services externes permettent d'accéder rapidement à des capacités IA avancées, mais introduisent des contraintes supplémentaires : coûts variables, dépendance fournisseur, gestion de clés, transfert de données et configuration cloud.

### Impact sur le projet

Le besoin actuel ne nécessite pas obligatoirement une infrastructure externe. Un service cloud pourrait devenir intéressant si les besoins augmentent en complexité ou en volume.

### Décision projet

**SURVEILLER — conserver les services externes dans le benchmark, sans les utiliser comme solution principale pour le POC.**

---

## 3.3. FastAPI et OpenAPI

### Constat

FastAPI répond au besoin d'exposer les données et le modèle IA via une API REST documentée. La génération OpenAPI facilite les tests, la documentation et l'intégration frontend.

### Impact sur le projet

Le framework est utilisé par :
- l'API métier ;
- l'API IA ;
- la sécurité par clé API ;
- Swagger ;
- les routes de monitoring.

### Décision projet

**CONSERVER — FastAPI reste le framework backend du projet.**

Les versions et changements de dépendances doivent continuer à être suivis via documentation officielle et GitHub Releases.

---

## 3.4. Sécurité API / OWASP

### Constat

Les API exposant des données ou un modèle doivent limiter les accès, valider les entrées et gérer les erreurs sans exposer inutilement des informations internes.

### Impact sur le projet

Les routes métier et IA sont protégées par `X-API-Key`. Le frontend doit tester une route réellement protégée pour vérifier la clé, et non une route publique comme `/health`.

### Décision projet

**DOCUMENTER ET SURVEILLER.**

Le mécanisme actuel est cohérent avec un POC local. Une version production nécessiterait notamment une authentification plus robuste, une gestion des rôles, HTTPS et une gestion sécurisée des secrets.

---

## 3.5. RGPD et minimisation

### Constat

Même si les données du POC sont simulées, une future intégration à une plateforme réelle pourrait traiter des commentaires, identifiants, données de commande et traces techniques rattachables à des personnes.

### Impact sur le projet

Le projet doit anticiper :
- minimisation ;
- pseudonymisation ;
- durée de conservation ;
- tri des données personnelles ;
- contrôle des logs ;
- gestion des demandes de suppression.

### Décision projet

**DOCUMENTER.**

Une procédure de tri des données personnelles est maintenue dans la documentation RGPD. Elle serait activée avant l'utilisation de données réelles.

---

## 3.6. AI Act et transparence

### Constat

L'évolution de la réglementation européenne renforce l'intérêt de documenter le fonctionnement, les limites, les données utilisées et la supervision d'un système IA.

### Impact sur le projet

Le rapport documente :
- la finalité du modèle ;
- les métriques ;
- les limites ;
- les données simulées ;
- la supervision humaine des prédictions peu confiantes ;
- le monitoring.

### Décision projet

**SURVEILLER ET DOCUMENTER.**

Les évolutions réglementaires doivent faire l'objet d'une revue périodique avant une intégration réelle.

---

## 3.7. Monitoring et MLOps

### Constat

Un modèle intégré dans une application doit pouvoir être testé, observé et reconstruit de manière reproductible.

### Impact sur le projet

Le projet dispose de :
- logs de prédiction ;
- métriques ;
- seuil de faible confiance ;
- dashboard ;
- alertes ;
- tests automatisés ;
- workflow GitHub Actions.

### Décision projet

**CONSERVER ET FAIRE ÉVOLUER.**

Les prochaines évolutions concernent notamment la couverture de tests, le packaging, la livraison et le monitoring applicatif.

---

## 3.8. Accessibilité

### Constat

L'accessibilité concerne à la fois l'application et les documents communiqués aux parties prenantes.

### Impact sur le projet

Les synthèses doivent rester lisibles en Markdown et lors de leur export PDF. Le frontend utilise des éléments HTML sémantiques, des labels, des messages textuels et une mise en page responsive.

### Décision projet

**DOCUMENTER ET TESTER.**

Les critères d'acceptation applicatifs doivent citer explicitement le référentiel d'accessibilité retenu.

---

## 3.9. Éco-conception

### Constat

Le choix d'outils proportionnés permet de réduire la complexité technique et l'utilisation de ressources inutiles.

### Impact sur le projet

Plusieurs choix vont dans cette direction :
- modèle ML léger ;
- frontend HTML/CSS/JavaScript natif ;
- absence de framework frontend lourd ;
- Nginx Alpine ;
- exécution locale du modèle ;
- limitation des appels à des services IA externes.

### Décision projet

**CONSERVER ET MESURER.**

Une mesure type EcoIndex pourra compléter les preuves d'éco-conception du frontend.

---

# 4. Revue mensuelle

À la fin de chaque mois, les entrées du journal sont relues afin de répondre aux questions suivantes :

- une dépendance doit-elle être mise à jour ?
- un risque réglementaire doit-il être ajouté ?
- un service doit-il être intégré au benchmark ?
- un choix technique doit-il être remis en question ?
- un ticket Jira doit-il être créé ?
- une documentation doit-elle être mise à jour ?

### Modèle de conclusion mensuelle

**Période :**  
**Nombre de séances réalisées :**  
**Temps total de veille :**  
**Décisions prises :**  
**Tickets Jira créés :**  
**Risques à surveiller le mois suivant :**

---

# 5. Partage et accessibilité

Les synthèses sont conservées au format Markdown dans le dépôt Git.

Pour une communication formelle, une version PDF peut être générée en respectant les règles suivantes :
- titres hiérarchisés ;
- texte sélectionnable ;
- tableaux simples ;
- contrastes suffisants ;
- liens explicites ;
- texte alternatif pour les illustrations ;
- absence d'information transmise uniquement par couleur.

Le partage peut être réalisé auprès :
- du référent pédagogique ;
- du commanditaire ou représentant métier ;
- de pairs lors d'une revue technique ;
- du jury via le rapport professionnel.

---

# 6. Preuves à conserver

Pour démontrer la réalisation de la veille :

1. `23a_plan_de_veille.md` ;
2. `23b_journal_de_veille.csv` complété avec les séances **réellement réalisées** ;
3. `23c_syntheses_de_veille.md` ;
4. captures Feedly / RSS ;
5. captures GitHub Releases ;
6. newsletters officielles utilisées ;
7. PDF accessible d'une synthèse si partagé ;
8. tickets Jira ou commits issus d'une décision de veille.

---

# 7. Important — intégrité du journal

Les lignes `PLANIFIÉE` du journal servent à organiser la récurrence hebdomadaire et ne constituent pas une preuve d'activité passée.

Après chaque séance réellement effectuée :
1. compléter le résumé ;
2. compléter la décision projet ;
3. renseigner la vérification de la source ;
4. indiquer le partage réalisé ;
5. passer le statut de `PLANIFIÉE` à `RÉALISÉE`.

Si une séance passée est reconstituée à partir de preuves existantes, utiliser le statut :

```text
RECONSTITUÉE À PARTIR DE PREUVES
```

et indiquer la preuve utilisée dans la colonne `Action / ticket`.
