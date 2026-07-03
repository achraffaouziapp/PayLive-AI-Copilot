# Contexte du projet — PayLive AI Copilot

## 1. Présentation générale du projet

Le projet **PayLive AI Copilot** consiste à concevoir une application web intelligente destinée aux vendeurs réalisant des ventes en direct sur des plateformes sociales comme TikTok Live ou Instagram Live.

Pendant une session de vente en direct, les vendeurs reçoivent un grand nombre de commentaires, de questions, de demandes de prix, de réservations de produits et de confirmations d’achat. Ces informations sont souvent dispersées, non structurées et difficiles à exploiter en temps réel.

L’objectif du projet est de centraliser ces données, de les structurer, puis de les rendre exploitables par une application et par un futur service d’intelligence artificielle capable d’analyser les intentions d’achat dans les commentaires.

## 2. Problématique métier

Les vendeurs en live shopping peuvent perdre des ventes à cause de plusieurs problèmes :

* volume important de commentaires pendant les lives ;
* difficulté à identifier rapidement les vrais acheteurs ;
* erreurs dans la prise de commande ;
* oubli de certaines demandes clients ;
* difficulté à suivre les paniers et les paiements ;
* absence de statistiques fiables après le live ;
* données clients et ventes dispersées dans plusieurs fichiers ou outils.

Le projet vise donc à construire une chaîne de données fiable permettant de collecter, nettoyer, stocker et exposer les informations nécessaires au suivi des ventes en live.

## 3. Objectif du Bloc 1

L’objectif du Bloc 1 est de mettre en place une chaîne complète de gestion des données du projet :

* collecte de données depuis plusieurs sources ;
* nettoyage et normalisation des données ;
* suppression des doublons et des données corrompues ;
* agrégation des données dans un jeu de données final ;
* stockage dans une base de données relationnelle ;
* conformité avec le RGPD ;
* mise à disposition des données via une API REST sécurisée et documentée.

Cette première partie ne traite pas encore du modèle d’intelligence artificielle. Elle prépare les données nécessaires pour les blocs suivants.

## 4. Utilisateurs concernés

Les utilisateurs principaux du système sont :

* les vendeurs réalisant des lives commerciaux ;
* les administrateurs de la plateforme ;
* les équipes support ;
* les équipes techniques ;
* les futurs composants applicatifs ou IA qui consommeront les données via API.

## 5. Données manipulées

Le projet manipule plusieurs familles de données :

* données vendeurs ;
* sessions live ;
* commentaires de live ;
* produits présentés pendant les lives ;
* paniers clients ;
* commandes ;
* paiements ;
* événements techniques ;
* statistiques de performance.

Aucune donnée réelle de l’entreprise PayLive n’est utilisée dans ce projet. Les données utilisées sont issues de sources publiques de test ou simulées selon les besoins du projet.

## 6. Choix de simulation des données

Comme aucune donnée réelle d’entreprise n’est disponible, le projet repose sur une stratégie de simulation réaliste.

Les données simulées intégreront volontairement des défauts afin de démontrer les étapes de nettoyage et de contrôle qualité :

* doublons ;
* valeurs manquantes ;
* formats de dates différents ;
* fautes de saisie ;
* statuts incohérents ;
* emails invalides ;
* montants incorrects ;
* plateformes mal nommées ;
* tailles et couleurs non normalisées ;
* références produits absentes ou incorrectes.

Ces défauts permettront de justifier les règles de nettoyage et d’agrégation mises en place dans le projet.

## 7. Résultat attendu du Bloc 1

À la fin du Bloc 1, le projet devra fournir :

* des scripts fonctionnels de collecte ;
* des fichiers de données brutes ;
* des fichiers nettoyés ;
* un dataset final agrégé ;
* une base de données PostgreSQL ;
* un modèle de données Merise ;
* des requêtes SQL documentées ;
* un script d’import en base ;
* une API REST sécurisée ;
* une documentation technique ;
* une documentation RGPD ;
* un dépôt Git contenant le code et les livrables.

## 8. Positionnement dans le projet global

Le Bloc 1 constitue la fondation technique du projet PayLive AI Copilot.

Les données préparées dans ce bloc seront utilisées ensuite pour :

* entraîner ou tester un modèle IA ;
* détecter les intentions d’achat dans les commentaires ;
* générer des paniers automatiquement ;
* suivre les paiements ;
* afficher des statistiques dans l’application ;
* alimenter les tableaux de bord de monitoring.
