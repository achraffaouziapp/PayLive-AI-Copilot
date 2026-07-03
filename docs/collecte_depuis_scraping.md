# Collecte par scraping web — Bloc 1

## 1. Objectif

Cette étape a pour objectif d’automatiser la collecte de données depuis des pages web.

Dans le cadre du projet PayLive AI Copilot, cette source permet de simuler l’extraction d’informations produits depuis un site web public de test.

## 2. Source utilisée

La source utilisée est Books to Scrape.

Il s’agit d’un site de démonstration conçu pour pratiquer le scraping web. Les données collectées sont fictives et ne représentent pas une activité commerciale réelle.

## 3. Script utilisé

Le script utilisé est :

`src/data_collection/collect_from_scraping.py`

## 4. Données collectées

Les données collectées concernent des produits :

- nom du produit ;
- catégorie ;
- description ;
- prix ;
- disponibilité ;
- stock disponible ;
- note ;
- URL de la fiche produit ;
- URL de l’image ;
- UPC brut ;
- page source.

## 5. Traitement réalisé

Le script réalise les actions suivantes :

- téléchargement des pages HTML ;
- sauvegarde des pages HTML brutes ;
- extraction des cartes produits ;
- accès aux pages détail des produits ;
- extraction des informations complémentaires ;
- ajout de métadonnées d’extraction ;
- sauvegarde des données extraites en CSV ;
- génération d’un manifeste d’extraction ;
- génération d’un rapport de schéma ;
- génération d’un rapport par page ;
- génération d’un rapport d’erreurs ;
- journalisation de l’exécution.

## 6. Sorties générées

Les sorties générées sont :

- `data/raw/products_scraped_raw.csv`
- `data/raw/scraping_html/*.html`
- `data/interim/scraping_extracts/products_scraped_extract.csv`
- `data/interim/scraping_extraction_manifest.csv`
- `data/interim/scraping_extraction_schema_report.csv`
- `data/interim/scraping_extraction_page_report.csv`
- `data/interim/scraping_extraction_errors.csv`
- `logs/collect_from_scraping.log`

## 7. Précautions

Aucun scraping n’est réalisé sur TikTok, Instagram ou un site marchand réel sans autorisation.

Le scraping est limité à un faible nombre de pages et intègre un délai entre les requêtes.

## 8. Justification

Cette étape permet de démontrer la capacité à automatiser l’extraction de données depuis une page web.

Elle complète les autres sources de collecte : fichiers CSV, API REST, base SQL source et source big data simulée.

## 9. Limite

Cette étape ne réalise pas de nettoyage métier.

Les données sont extraites depuis le HTML et conservées avec leurs valeurs brutes. Les transformations, normalisations et contrôles qualité seront appliqués dans les scripts de nettoyage.