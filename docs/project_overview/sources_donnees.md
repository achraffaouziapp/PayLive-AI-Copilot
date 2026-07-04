# Sources de données — Bloc 1

## 1. Objectif du document

Ce document présente les sources de données utilisées dans le Bloc 1 du projet PayLive AI Copilot.

Comme aucune donnée réelle de l’entreprise n’est disponible, les données utilisées sont soit issues de sources publiques de test, soit simulées pour répondre aux besoins du projet.

L’objectif est de disposer de données réalistes permettant de démontrer les compétences de collecte, nettoyage, agrégation, stockage et mise à disposition via API.

## 2. Principe général

Les données seront volontairement hétérogènes afin de reproduire un contexte réaliste.

Les sources utilisées seront de plusieurs types :

* API REST externe ;
* fichiers CSV ;
* fichiers JSON ;
* scraping autorisé ;
* base de données SQL source ;
* fichiers de logs volumineux au format Parquet.

Cette diversité permet de couvrir plusieurs modes de collecte et d’extraction.

## 3. Source 1 — API externe de produits

### Description

Une API publique de test sera utilisée pour récupérer un catalogue de produits fictifs.

### Données récupérées

Les données récupérées pourront contenir :

* identifiant produit ;
* nom du produit ;
* catégorie ;
* description ;
* prix ;
* stock ;
* marque ;
* note ;
* image.

### Utilité dans le projet

Ces données permettront de construire le catalogue produit utilisé pendant les lives.

### Défauts attendus ou ajoutés

Après collecte, certaines anomalies pourront être ajoutées volontairement :

* doublons de produits ;
* prix manquants ;
* catégories non normalisées ;
* noms de produits avec casse différente ;
* stocks négatifs ou incohérents.

## 4. Source 2 — Fichiers CSV simulés

### Description

Des fichiers CSV seront générés pour simuler les données produites par l’activité de live shopping.

### Fichiers prévus

Les fichiers suivants seront créés :

* `sellers_raw.csv` ;
* `live_sessions_raw.csv` ;
* `live_comments_raw.csv` ;
* `payments_raw.csv` ;
* `stock_movements_raw.csv`.

### Données simulées

Ces fichiers contiendront :

* vendeurs ;
* sessions live ;
* commentaires ;
* paiements ;
* mouvements de stock.

### Défauts volontairement intégrés

Les fichiers contiendront volontairement :

* lignes dupliquées ;
* identifiants manquants ;
* dates invalides ;
* emails invalides ;
* plateformes mal nommées ;
* montants incohérents ;
* statuts contradictoires ;
* valeurs textuelles non normalisées.

## 5. Source 3 — Scraping d’un site de test

### Description

Un site de test autorisé pour le scraping sera utilisé afin de récupérer des informations produits complémentaires.

### Données récupérées

Les données récupérées pourront contenir :

* nom du produit ;
* prix ;
* catégorie ;
* description ;
* URL de la fiche produit.

### Utilité dans le projet

Cette source permettra de démontrer la capacité à collecter des données depuis une page web.

### Précaution

Aucun scraping ne sera réalisé sur TikTok, Instagram ou un site marchand réel sans autorisation.

## 6. Source 4 — Base SQL source simulée

### Description

Une base de données source fictive sera créée pour représenter un ancien système de gestion des ventes.

### Tables prévues

La base source pourra contenir :

* `legacy_sellers` ;
* `legacy_orders` ;
* `legacy_payments` ;
* `legacy_live_sessions`.

### Utilité dans le projet

Cette source permettra de démontrer l’écriture et l’exécution de requêtes SQL d’extraction.

### Exemples de requêtes attendues

Les requêtes SQL permettront de :

* récupérer les commandes d’une période donnée ;
* filtrer les paiements validés ;
* joindre les commandes avec les vendeurs ;
* calculer le chiffre d’affaires par session live ;
* identifier les commandes incomplètes.

## 7. Source 5 — Logs big data simulés

### Description

Des fichiers de logs volumineux seront simulés au format Parquet.

### Données prévues

Les logs pourront contenir :

* événement de commentaire ;
* clic sur lien de paiement ;
* ouverture de panier ;
* validation de paiement ;
* erreur API ;
* abandon de panier.

### Utilité dans le projet

Cette source permettra de montrer une logique de traitement big data avec PySpark.

### Traitements prévus

Les traitements pourront inclure :

* lecture de fichiers Parquet ;
* filtrage des événements ;
* agrégation par live ;
* calcul du nombre de commentaires ;
* calcul du nombre de clics paiement ;
* calcul du taux d’abandon panier.

## 8. Justification du choix des sources

Le choix de ces sources permet de couvrir un périmètre complet de collecte de données :

* API REST pour les données structurées externes ;
* fichiers CSV/JSON pour les exports métier ;
* scraping pour les données web ;
* base SQL pour les systèmes existants ;
* fichiers Parquet pour les logs volumineux.

Cette diversité permet de simuler un environnement professionnel réaliste et de préparer les données nécessaires aux futurs blocs du projet.

## 9. Traçabilité des données

Chaque fichier produit devra être traçable.

Pour chaque source, la documentation précisera :

* origine de la donnée ;
* méthode de collecte ;
* date de collecte ;
* script utilisé ;
* format du fichier ;
* emplacement du fichier brut ;
* traitements appliqués ;
* emplacement du fichier nettoyé.

## 10. Limites

Les données étant simulées, elles ne représentent pas l’activité réelle de l’entreprise.

Cependant, elles sont construites pour reproduire des problématiques réalistes :

* qualité variable ;
* hétérogénéité des formats ;
* erreurs de saisie ;
* doublons ;
* données manquantes ;
* incohérences métier.

Ces limites seront mentionnées dans le rapport afin de rester transparent sur le périmètre du projet.
