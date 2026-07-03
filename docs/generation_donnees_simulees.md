# Génération des données simulées — Bloc 1

## 1. Objectif

Ce document décrit la génération des données brutes simulées utilisées dans le Bloc 1 du projet PayLive AI Copilot.

Comme aucune donnée réelle de l’entreprise n’est utilisée, les données sont générées artificiellement afin de représenter un contexte réaliste de ventes en live sur TikTok ou Instagram.

## 2. Justification

La simulation des données permet de créer un environnement contrôlé pour démontrer les compétences suivantes :

* collecte de données depuis des fichiers ;
* préparation de données brutes ;
* détection des doublons ;
* traitement des valeurs manquantes ;
* correction des formats invalides ;
* normalisation des valeurs ;
* contrôle de cohérence ;
* agrégation des données ;
* préparation au stockage en base PostgreSQL.

## 3. Fichiers générés

Le script `src/data_simulation/generate_raw_data.py` génère les fichiers suivants dans le dossier `data/raw` :

* `sellers_raw.csv` ;
* `customers_raw.csv` ;
* `products_raw.csv` ;
* `live_sessions_raw.csv` ;
* `live_products_raw.csv` ;
* `live_comments_raw.csv` ;
* `carts_raw.csv` ;
* `cart_items_raw.csv` ;
* `orders_raw.csv` ;
* `payments_raw.csv` ;
* `stock_movements_raw.csv` ;
* `live_events_raw.csv` ;
* `data_quality_issues_summary.csv`.

## 4. Défauts volontairement injectés

Les données contiennent volontairement plusieurs types d’anomalies :

* doublons d’identifiants ;
* doublons de lignes ;
* valeurs manquantes ;
* dates invalides ;
* formats de dates hétérogènes ;
* emails invalides ;
* plateformes non normalisées ;
* statuts non reconnus ;
* montants négatifs ;
* devises invalides ;
* références inexistantes ;
* incohérences entre montants de panier, commande et paiement ;
* quantités de stock incohérentes ;
* tailles et couleurs non normalisées ;
* commentaires vides ou ambigus.

## 5. Rôle dans la chaîne de données

Ces fichiers représentent la couche brute du projet.

Ils seront ensuite utilisés pour :

* analyser la qualité des données ;
* écrire les règles de nettoyage ;
* produire les fichiers intermédiaires ;
* produire les fichiers nettoyés ;
* créer le dataset final ;
* alimenter la base PostgreSQL ;
* exposer les données via une API REST.

## 6. Traçabilité

Les données brutes sont conservées dans le dossier `data/raw`.

Aucune modification directe ne doit être réalisée sur ces fichiers. Les corrections seront effectuées par des scripts dédiés, avec des sorties dans les dossiers `data/interim` puis `data/processed`.

## 7. Limites

Les données générées ne représentent pas l’activité réelle de PayLive.

Elles sont conçues pour simuler des problématiques réalistes de qualité de données dans un contexte de live shopping.
