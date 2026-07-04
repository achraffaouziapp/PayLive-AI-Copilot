# Bilan Bloc 3 — Application intégrant le service IA PayLive AI Copilot

## 1. Objectif du document

Ce document sert de bilan pour le Bloc 3 du projet **PayLive AI Copilot**.

Il sera mis à jour à la fin du développement de l’application frontend HTML/CSS/JavaScript.

La version actuelle constitue un bilan prévisionnel et une grille de suivi permettant de vérifier que les compétences du Bloc 3 sont couvertes progressivement.

## 2. Objectif du Bloc 3

Le Bloc 3 consiste à réaliser une application web intégrant le service IA développé dans le Bloc 2.

L’objectif est de passer d’un service IA exposé par API à une interface utilisateur exploitable par un vendeur ou un responsable métier.

Application prévue :

```text
PayLive AI Copilot Frontend
```

Technologies retenues :

```text
HTML
CSS
JavaScript natif
Nginx
Docker Compose
FastAPI existante
```

## 3. Réalisations prévues

| Réalisation | Statut |
|---|---|
| Cadrage application | Prévu / en cours |
| Spécifications fonctionnelles | Prévu / en cours |
| Architecture technique | Prévu / en cours |
| User stories et accessibilité | Prévu / en cours |
| Interface HTML/CSS/JS | À développer |
| Conteneur Docker frontend | À développer |
| Intégration API IA | À développer |
| Tests application | À développer |
| Documentation finale | À compléter |

## 4. Fonctionnalités cibles

L’application doit permettre de :

```text
saisir une clé API
saisir un commentaire de live
appeler le service IA
voir l’intention prédite
voir le score de confiance
identifier les prédictions faibles
analyser plusieurs commentaires
consulter les informations du modèle
consulter les métriques du modèle
accéder au dashboard IA
consulter ou télécharger les alertes IA
```

## 5. Couverture prévisionnelle des compétences

| Compétence / attendu | Mise en œuvre prévue |
|---|---|
| Analyse du besoin applicatif | Documents 31 et 32 |
| Spécifications fonctionnelles | User stories et critères de validation |
| Modélisation des parcours | Parcours utilisateur et wireframe textuel |
| Accessibilité | Critères d’acceptation intégrant labels, clavier, contraste, `aria-live` |
| Cadre technique | Architecture Docker + HTML/JS + FastAPI |
| Flux de données | Diagrammes de flux frontend → API → modèle → monitoring |
| Développement interface | Fichiers `frontend/public` |
| Intégration API IA | Appels `fetch` vers les routes IA |
| Authentification API | Header `X-API-Key` envoyé côté frontend |
| Tests d’intégration | Tests manuels et automatisés prévus |
| Livraison application | Docker Compose + Git + documentation |

## 6. Architecture retenue

```text
Navigateur
   ↓
Frontend HTML/CSS/JS dans Docker Nginx
   ↓
API FastAPI dans Docker
   ↓
Service IA local
   ↓
Modèle TF-IDF + Logistic Regression
   ↓
Monitoring et alertes
```

Cette architecture est simple, locale, reproductible et adaptée à une démonstration de fin d’études.

## 7. Justification du choix HTML/CSS/JS

Le choix de HTML/CSS/JavaScript natif est cohérent car :

- il limite les dépendances ;
- il facilite la lecture du code ;
- il permet une démonstration rapide ;
- il s’intègre facilement avec Docker et Nginx ;
- il évite un framework trop lourd pour une preuve de concept ;
- il met en évidence les appels API réalisés ;
- il permet d’intégrer les règles d’accessibilité de base.

## 8. Preuves à produire à la fin du Bloc 3

| Preuve | Emplacement ou support prévu |
|---|---|
| Interface chargée | Capture `http://localhost:8080` |
| Prédiction simple | Capture résultat IA |
| Prédiction batch | Capture tableau batch |
| Clé API invalide | Capture erreur 403 |
| Infos modèle | Capture section modèle |
| Métriques modèle | Capture section métriques |
| Dashboard IA | Capture dashboard ouvert depuis le front |
| Alertes IA | Capture ou CSV téléchargé |
| Docker Compose | Capture `docker compose ps` |
| Tests application | Rapport ou sortie terminal |
| Versionnement Git | Commit final |

## 9. Difficultés anticipées

| Difficulté | Solution prévue |
|---|---|
| Problème CORS | Ajouter `CORSMiddleware` dans FastAPI |
| Clé API non envoyée | Centraliser les appels dans `apiFetch()` |
| API arrêtée | Afficher un message “API inaccessible” |
| Dashboard protégé par API key | Charger le HTML via `fetch` avec header |
| Interface peu accessible | Tests clavier, labels et `aria-live` |
| Docker frontend non accessible | Vérifier ports et logs Nginx |

## 10. Limites de la première version

La première version ne couvrira pas :

```text
authentification multi-utilisateur
rôles et permissions avancés
connexion réelle à TikTok ou Instagram
analyse en temps réel de flux live
stockage d’historique côté frontend
front React ou Vue
mode production sécurisé complet
```

Ces limites sont acceptées car le Bloc 3 vise une preuve de concept applicative intégrée au service IA.

## 11. Évolutions possibles

Évolutions futures :

- ajouter un vrai système d’authentification utilisateur ;
- créer un tableau de bord vendeur plus complet ;
- intégrer un flux de commentaires simulé en temps réel ;
- ajouter l’extraction produit / taille / couleur / quantité ;
- ajouter des retours utilisateur pour améliorer les labels ;
- intégrer une interface d’administration ;
- améliorer la CI avec tests frontend automatisés ;
- préparer un déploiement cloud.

## 12. Critères de clôture du Bloc 3

Le Bloc 3 pourra être clôturé lorsque :

- l’application frontend est fonctionnelle ;
- Docker Compose lance l’API et le frontend ;
- les appels API IA fonctionnent depuis l’interface ;
- les résultats IA sont affichés ;
- la clé API est gérée ;
- les erreurs sont affichées ;
- le dashboard et les alertes sont accessibles ;
- les tests sont réalisés ;
- les preuves sont capturées ;
- la documentation est mise à jour ;
- le code est versionné dans Git.

## 13. Conclusion provisoire

Le cadrage du Bloc 3 définit une application web simple et cohérente avec les deux premiers blocs.

Cette application permettra de démontrer concrètement l’usage du service IA dans un contexte métier de live shopping.

À la fin du développement, ce document devra être mis à jour avec :

```text
les fonctionnalités réellement développées
les résultats des tests
les captures d’écran
les difficultés rencontrées
les corrections réalisées
le bilan final de couverture des compétences
```
