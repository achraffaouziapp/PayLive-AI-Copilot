# Plan de veille technique et réglementaire IA

## 1. Objectif

La veille a pour objectif de maintenir les choix techniques et réglementaires du projet en phase avec l'état de l'art, tout en conservant une démarche proportionnée au besoin, au budget et au niveau de maturité du POC.

Elle couvre les composants réellement mobilisés dans le projet : classification NLP, scikit-learn, FastAPI, sécurité API, RGPD, AI Act, monitoring, MLOps, Docker, PostgreSQL, accessibilité et éco-conception.

La veille doit aboutir à des **décisions projet explicites** : conserver une solution, la faire évoluer, surveiller un risque, tester une alternative ou documenter une contrainte.

---

## 2. Récurrence et durée

- **Récurrence : chaque mercredi**
- **Durée minimale : 1 heure**
- **Créneau conseillé : 09h00–10h00**
- **Fréquence : hebdomadaire**
- **Revue de synthèse : fin de chaque mois**
- **Revue exceptionnelle : en cas de changement réglementaire, faille de sécurité, nouvelle version majeure ou évolution importante du service IA**

Le journal `23b_journal_de_veille.csv` doit être complété après chaque séance réellement réalisée.

> Important : une séance planifiée mais non réalisée doit rester indiquée comme `PLANIFIÉE` et ne doit pas être présentée comme une séance effectuée.

---

## 3. Thématiques suivies

| Axe | Sujets suivis | Impact possible sur le projet |
|---|---|---|
| NLP / Machine Learning | classification de texte, TF-IDF, Logistic Regression, modèles Transformers | choix ou évolution du modèle |
| scikit-learn | versions, métriques, bonnes pratiques, sécurité des artefacts | entraînement et inférence |
| FastAPI / OpenAPI | versions, validation, documentation, performance | API métier et IA |
| Sécurité | OWASP API Security, dépendances, authentification | sécurisation de l'API et du frontend |
| RGPD / CNIL | minimisation, conservation, pseudonymisation | traitement des données |
| AI Act | transparence, documentation, responsabilités | cadre réglementaire IA |
| MLOps | tests, packaging, versionnement, CI/CD | reproductibilité et livraison |
| Monitoring IA | dérive, qualité des prédictions, latence, alertes | amélioration du modèle |
| Docker / Nginx | versions, sécurité, images légères | exécution et déploiement |
| PostgreSQL | versions, indexation, optimisation | stockage et performances |
| Accessibilité | WCAG / RGAA, documents et interfaces | critères d'acceptation |
| Éco-conception | sobriété logicielle, EcoIndex / GreenIT | choix techniques proportionnés |

---

## 4. Outils de collecte et d'agrégation

La veille repose sur des outils simples, peu coûteux et adaptés à un projet individuel.

### Feedly / RSS

Feedly ou un lecteur RSS équivalent sert à regrouper les flux de sources officielles et techniques.

Utilisation :
- centraliser plusieurs sources ;
- éviter de visiter manuellement chaque site ;
- repérer les nouvelles publications ;
- classer les sources par thème.

### Newsletters officielles

Les newsletters officielles sont utilisées lorsqu'elles sont proposées par les éditeurs ou institutions.

Exemples de thèmes :
- sécurité ;
- réglementation ;
- frameworks ;
- cloud / IA ;
- accessibilité.

### GitHub Releases

Les pages `Releases` des projets utilisés sont suivies afin de détecter :
- nouvelles versions ;
- correctifs de sécurité ;
- dépréciations ;
- changements d'API ;
- breaking changes.

Projets particulièrement concernés :
- FastAPI ;
- scikit-learn ;
- Uvicorn ;
- Docker-related tooling lorsque pertinent.

### Documentation officielle

La documentation officielle reste la source privilégiée pour toute décision technique importante.

---

## 5. Sélection et fiabilité des sources

Une source n'est intégrée à une synthèse que si elle satisfait au maximum les critères suivants :

1. auteur ou organisme identifié ;
2. compétence ou légitimité de l'auteur vérifiable ;
3. date de publication ou de mise à jour disponible ;
4. contenu structuré et compréhensible ;
5. sources ou références disponibles lorsque nécessaire ;
6. information confirmable par une autre source de confiance ;
7. préférence donnée aux documentations officielles, institutions, standards et dépôts officiels ;
8. préférence donnée aux ressources accessibles.

### Hiérarchie de confiance

**Niveau 1 — prioritaire**
- documentation officielle ;
- texte réglementaire officiel ;
- institution publique ;
- standard reconnu ;
- dépôt GitHub officiel.

**Niveau 2 — complémentaire**
- article technique d'un éditeur reconnu ;
- publication d'un expert identifié ;
- documentation d'un fournisseur.

**Niveau 3 — inspiration uniquement**
- blog non officiel ;
- forum ;
- publication communautaire non vérifiée.

Une information de niveau 3 ne doit pas être utilisée seule pour justifier une décision importante.

---

## 6. Déroulement d'une séance hebdomadaire

Chaque séance d'une heure suit le même déroulement.

### 0–10 minutes — collecte

- consulter Feedly / RSS ;
- vérifier les newsletters ;
- consulter les GitHub Releases ;
- sélectionner les informations pertinentes.

### 10–35 minutes — lecture et vérification

- lire les sources sélectionnées ;
- vérifier l'auteur et la date ;
- croiser l'information si elle a un impact important ;
- identifier les changements utiles au projet.

### 35–50 minutes — analyse projet

Répondre aux questions :
- cette information modifie-t-elle un choix actuel ?
- existe-t-il un risque de sécurité ou de conformité ?
- une dépendance doit-elle être mise à jour ?
- une alternative mérite-t-elle un benchmark ?
- faut-il créer une tâche Jira ?

### 50–60 minutes — journal et partage

- compléter `23b_journal_de_veille.csv` ;
- mettre à jour `23c_syntheses_de_veille.md` si nécessaire ;
- identifier la décision projet ;
- partager la synthèse aux parties prenantes concernées.

---

## 7. Informations obligatoires du journal

Chaque entrée réellement effectuée contient au minimum :

- **Date**
- **Durée**
- **Sujet**
- **Source**
- **Résumé**
- **Décision projet**

Des champs complémentaires sont ajoutés :
- canal / outil ;
- niveau de fiabilité ;
- action ou ticket Jira ;
- mode de partage ;
- statut.

---

## 8. Partage des synthèses

### Format principal

Les synthèses sont partagées en **Markdown**, directement dans le dépôt Git :

```text
docs/ai_service/23c_syntheses_de_veille.md
```

Avantages :
- texte structuré ;
- versionnement Git ;
- recherche facile ;
- lecture possible sans logiciel propriétaire ;
- mise à jour simple.

### Format de diffusion

Lorsque nécessaire, une version **PDF accessible** peut être produite à partir de la synthèse Markdown pour la soutenance ou le partage aux parties prenantes.

### Parties prenantes visées

Selon le contexte et les disponibilités :
- référent pédagogique ;
- commanditaire / représentant métier ;
- autres membres ou pairs participant aux revues techniques ;
- jury via le rapport professionnel.

Le projet étant réalisé principalement de manière individuelle, la collecte et la synthèse sont pilotées par le candidat. Le partage et les retours des parties prenantes permettent toutefois de confronter les décisions techniques et réglementaires.

---

## 9. Règles d'accessibilité des synthèses

Les synthèses Markdown et PDF doivent rester utilisables par le plus grand nombre.

Règles appliquées :
- hiérarchie correcte des titres ;
- phrases courtes et langage explicite ;
- liens accompagnés d'un libellé compréhensible ;
- tableaux simples avec en-têtes ;
- ne pas utiliser uniquement la couleur pour transmettre une information ;
- texte alternatif pour les images lorsque des illustrations sont ajoutées ;
- contraste suffisant dans les exports ;
- structure logique de lecture ;
- PDF généré avec texte sélectionnable et non sous forme d'image.

---

## 10. Lien entre veille et décisions projet

La veille n'a pas pour objectif de produire une liste de liens. Chaque information importante doit être reliée à une conséquence pour le projet.

Exemples :

| Information issue de la veille | Décision projet possible |
|---|---|
| une dépendance contient un correctif de sécurité important | planifier une mise à jour et exécuter les tests |
| une nouvelle exigence réglementaire concerne la transparence IA | enrichir la documentation du modèle |
| un service cloud devient pertinent pour un nouveau besoin | l'ajouter au benchmark |
| une solution est disproportionnée pour la classification actuelle | conserver le modèle local |
| une recommandation OWASP concerne l'API | créer une tâche de sécurisation |
| une évolution WCAG concerne un composant utilisé | mettre à jour les critères d'acceptation |

---

## 11. Traçabilité

Les trois documents de veille sont versionnés ensemble :

```text
docs/ai_service/
├── plan_de_veille.md
├── journal_de_veille.csv
└── syntheses_de_veille.md
```

Les décisions importantes peuvent également être reliées :
- à un ticket Jira ;
- à un commit Git ;
- à une modification de documentation ;
- à une évolution du benchmark ;
- à un test ou une mise à jour de dépendance.

---

## 12. Preuves recommandées pour le dossier

Captures à conserver :
1. dossier `docs/ai_service` avec les trois fichiers ;
2. journal CSV avec plusieurs séances réellement renseignées ;
3. capture Feedly / RSS ;
4. capture d'une page GitHub Releases suivie ;
5. exemple de newsletter officielle ;
6. synthèse Markdown ;
7. éventuel PDF accessible ;
8. ticket Jira ou commit directement issu d'une décision de veille.

---

## 13. Point de vigilance

Le journal doit refléter les séances **réellement réalisées**.

Il ne faut pas transformer rétroactivement des séances planifiées en séances réalisées sans preuve. Si des activités de veille ont déjà eu lieu pendant le projet mais n'ont pas été journalisées au moment de leur réalisation, elles peuvent être ajoutées comme **reconstitution documentaire**, en précisant clairement cette mention et en s'appuyant sur des éléments datés : commits, documents, historique navigateur, notes ou tickets Jira.
