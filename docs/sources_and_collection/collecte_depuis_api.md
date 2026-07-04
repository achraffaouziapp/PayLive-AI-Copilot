# Collecte depuis une API REST — Bloc 1

## 1. Objectif

Cette étape a pour objectif d’automatiser la collecte de données depuis une API REST externe.

Dans le cadre du projet PayLive AI Copilot, cette source permet de simuler la récupération d’un catalogue produit depuis un service web externe.

## 2. Source utilisée

La source utilisée est l’API publique de test DummyJSON.

Elle fournit des données fictives utiles pour le développement, les tests et le prototypage d’applications.

## 3. Script utilisé

Le script utilisé est :

`src/data_collection/collect_from_api.py`

## 4. Données collectées

Les données collectées concernent des produits :

- identifiant produit ;
- titre ;
- description ;
- catégorie ;
- prix ;
- remise ;
- note ;
- stock ;
- marque ;
- images ;
- informations de livraison ;
- disponibilité.

## 5. Traitement réalisé

Le script réalise les actions suivantes :

- appel HTTP vers l’API REST ;
- gestion des erreurs de connexion ;
- mécanisme de retry ;
- vérification du code de réponse HTTP ;
- sauvegarde de la réponse JSON brute ;
- extraction des produits dans un format tabulaire ;
- ajout de métadonnées d’extraction ;
- génération d’un manifeste d’extraction ;
- génération d’un rapport de schéma ;
- génération d’un rapport d’erreurs ;
- journalisation de l’exécution.

## 6. Sorties générées

Les sorties générées sont :

- `data/raw/products_api_raw.json`
- `data/interim/api_extracts/products_api_extract.csv`
- `data/interim/api_extraction_manifest.csv`
- `data/interim/api_extraction_schema_report.csv`
- `data/interim/api_extraction_errors.csv`
- `logs/collect_from_api.log`

## 7. Justification

Cette étape permet de démontrer la capacité à automatiser l’extraction de données depuis un service web externe.

Elle complète la collecte depuis fichiers CSV et prépare l’intégration du catalogue produit dans le dataset final.

## 8. Limite

Cette étape ne réalise pas de nettoyage métier.

Les données récupérées depuis l’API sont conservées telles quelles dans le fichier JSON brut. Les transformations de qualité seront appliquées dans les scripts de nettoyage et de normalisation.