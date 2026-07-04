# Collecte depuis fichiers CSV — Bloc 1

## 1. Objectif

Cette étape a pour objectif d’automatiser la collecte des données depuis des fichiers CSV locaux.

Les fichiers CSV représentent des exports métier simulés dans le cadre du projet PayLive AI Copilot.

## 2. Script utilisé

Le script utilisé est :

`src/data_collection/collect_from_files.py`

## 3. Données collectées

Les fichiers collectés sont :

- `sellers_raw.csv`
- `customers_raw.csv`
- `products_raw.csv`
- `live_sessions_raw.csv`
- `live_products_raw.csv`
- `live_comments_raw.csv`
- `carts_raw.csv`
- `cart_items_raw.csv`
- `orders_raw.csv`
- `payments_raw.csv`
- `stock_movements_raw.csv`
- `live_events_raw.csv`

## 4. Traitement réalisé

Le script réalise les actions suivantes :

- vérification de la présence des fichiers attendus ;
- lecture automatique des fichiers CSV ;
- chargement des données en conservant les valeurs brutes ;
- vérification des colonnes attendues ;
- ajout de métadonnées d’extraction ;
- sauvegarde des extractions dans `data/interim/file_extracts` ;
- génération d’un manifeste d’extraction ;
- génération d’un rapport de schéma ;
- génération d’un rapport d’erreurs ;
- journalisation de l’exécution.

## 5. Sorties générées

Les sorties générées sont :

- `data/interim/file_extraction_manifest.csv`
- `data/interim/file_extraction_schema_report.csv`
- `data/interim/file_extraction_errors.csv`
- `data/interim/file_extracts/*.csv`
- `logs/collect_from_files.log`

## 6. Justification

Cette étape permet de démontrer la capacité à automatiser la collecte de données depuis des fichiers structurés.

Elle prépare les étapes suivantes de nettoyage, normalisation, agrégation et import en base de données.

## 7. Limite

Cette étape ne réalise aucun nettoyage métier.

Les données sont extraites telles qu’elles sont présentes dans les fichiers sources. Les corrections seront appliquées dans les scripts de traitement dédiés.