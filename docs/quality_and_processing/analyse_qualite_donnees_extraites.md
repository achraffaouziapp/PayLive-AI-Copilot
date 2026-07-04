# Analyse qualité des données extraites — Bloc 1

## 1. Objectif du document

Ce document présente l’analyse qualité réalisée sur les données extraites dans le cadre du projet **PayLive AI Copilot**.

Après la collecte multi-sources, les données sont stockées dans des répertoires intermédiaires. Avant de lancer le nettoyage et la normalisation, il est nécessaire de contrôler la qualité des données extraites.

L’objectif est de vérifier :

```text
la présence des fichiers attendus
la structure des fichiers extraits
la présence des colonnes attendues
les valeurs manquantes
les doublons
les formats invalides
les incohérences métier
les problèmes de relations entre tables
les anomalies de dates
les anomalies financières
```

Cette étape permet de sécuriser la suite du pipeline avant le nettoyage et l’agrégation finale.

## 2. Position dans le pipeline Bloc 1

L’analyse qualité des données extraites intervient après les étapes de collecte :

```text
1. Génération des données simulées
2. Analyse qualité des données brutes
3. Collecte depuis fichiers CSV
4. Collecte depuis API externe
5. Collecte depuis scraping autorisé
6. Collecte depuis base SQL simulée
7. Collecte depuis source Big Data Parquet
8. Analyse qualité des données extraites
9. Nettoyage et normalisation
10. Agrégation du dataset final IA
```

Cette étape constitue donc un contrôle intermédiaire entre la collecte et le nettoyage.

## 3. Script utilisé

Le script utilisé est :

```text
src/data_processing/analyze_extracted_data_quality.py
```

Ce script lit les données extraites depuis les dossiers intermédiaires et produit plusieurs rapports de qualité.

## 4. Données analysées

Les données analysées proviennent des extractions suivantes :

```text
data/interim/file_extracts/
data/interim/api_extracts/
data/interim/scraping_extracts/
data/interim/database_extracts/
data/interim/bigdata_extracts/
```

Ces dossiers contiennent les données collectées depuis :

```text
fichiers CSV simulés
API REST externe
scraping autorisé
base SQL simulée
source Big Data Parquet
```

## 5. Objectifs de l’analyse qualité

L’analyse qualité poursuit plusieurs objectifs.

## 5.1. Vérifier la disponibilité des extractions

Le script vérifie que les fichiers attendus existent bien après chaque collecte.

Exemples de fichiers ou dossiers attendus :

```text
file_extracts
api_extracts
scraping_extracts
database_extracts
bigdata_extracts
```

Cette vérification permet de détecter rapidement une collecte manquante ou échouée.

## 5.2. Vérifier la structure des fichiers

Le script contrôle :

```text
le nombre de lignes
le nombre de colonnes
les colonnes présentes
les colonnes manquantes
les colonnes inattendues
le taux de valeurs manquantes
```

Cette étape permet de vérifier que les fichiers extraits respectent la structure attendue avant leur nettoyage.

## 5.3. Vérifier les valeurs manquantes

Le script calcule les valeurs manquantes par fichier et par colonne.

Les valeurs considérées comme manquantes peuvent être :

```text
valeur vide
NaN
None
null
chaîne vide
valeur textuelle équivalente à null
```

Les colonnes importantes sont particulièrement surveillées, par exemple :

```text
seller_id
customer_id
live_id
product_id
cart_id
order_id
payment_id
comment_text
```

## 5.4. Vérifier les doublons

Le script détecte les doublons sur les clés techniques.

Exemples :

```text
seller_id
customer_id
live_id
product_id
comment_id
cart_id
order_id
payment_id
event_id
```

La présence de doublons est importante à détecter avant l’import en base PostgreSQL, car les clés primaires doivent être uniques.

## 5.5. Vérifier les formats

Le script contrôle certains formats :

```text
emails
dates
nombres
montants
statuts
plateformes
devises
```

Exemples d’anomalies détectables :

```text
email sans arobase
date impossible
montant négatif
statut non autorisé
plateforme non normalisée
devise inconnue
```

## 5.6. Vérifier les règles métier

Le script applique des règles métier afin d’identifier les incohérences.

Exemples de règles :

```text
un panier ne doit pas avoir un montant négatif
une commande payée doit avoir un paiement cohérent
une date de fin de live ne doit pas être avant la date de début
une quantité commandée doit être positive
un paiement réussi doit avoir une date de paiement
un produit ne doit pas avoir un stock négatif
```

## 5.7. Vérifier les relations entre données

Le script vérifie aussi certaines relations entre tables.

Exemples :

```text
un live doit être rattaché à un vendeur existant
un commentaire doit être rattaché à un live existant
un panier doit être rattaché à un client existant
une commande doit être rattachée à un panier existant
un paiement doit être rattaché à une commande existante
un événement doit être rattaché à un live existant
```

Ces contrôles permettent d’anticiper les erreurs d’intégrité référentielle avant l’import PostgreSQL.

## 6. Rapports générés

Le script génère les rapports suivants :

```text
data/interim/extracted_quality_file_report.csv
data/interim/extracted_quality_column_report.csv
data/interim/extracted_quality_business_rules_report.csv
data/interim/extracted_quality_summary.csv
logs/analyze_extracted_data_quality.log
```

## 7. Description des rapports

## 7.1. `extracted_quality_file_report.csv`

Ce rapport contient une synthèse par fichier analysé.

Il indique notamment :

```text
nom du fichier
source de données
nombre de lignes
nombre de colonnes
statut du fichier
nombre total de valeurs manquantes
nombre de doublons détectés
message d’erreur éventuel
```

Ce rapport permet d’avoir une vue globale sur la qualité des fichiers extraits.

## 7.2. `extracted_quality_column_report.csv`

Ce rapport contient une analyse détaillée par colonne.

Il indique notamment :

```text
nom du fichier
nom de la colonne
type détecté
nombre de valeurs non nulles
nombre de valeurs manquantes
taux de valeurs manquantes
nombre de valeurs uniques
exemples de valeurs
```

Ce rapport permet d’identifier les colonnes les plus problématiques.

## 7.3. `extracted_quality_business_rules_report.csv`

Ce rapport contient les résultats des contrôles métier.

Il indique notamment :

```text
nom de la règle
table concernée
colonne concernée
nombre d’anomalies détectées
niveau de gravité
description du problème
```

Exemples de règles :

```text
duplicate_primary_key
invalid_email_format
invalid_date_format
negative_amount
invalid_status
invalid_foreign_key
end_date_before_start_date
payment_success_without_paid_at
```

## 7.4. `extracted_quality_summary.csv`

Ce rapport synthétise les résultats globaux de l’analyse.

Il permet d’obtenir rapidement :

```text
nombre total de fichiers analysés
nombre total de lignes analysées
nombre total d’anomalies détectées
nombre d’anomalies critiques
nombre d’anomalies non critiques
statut global de l’analyse
```

## 7.5. Log technique

Le fichier de log est :

```text
logs/analyze_extracted_data_quality.log
```

Il permet de tracer :

```text
le lancement du script
les fichiers analysés
les erreurs techniques éventuelles
les chemins utilisés
la fin de l’exécution
```

## 8. Types d’anomalies attendues

Les données du projet contiennent volontairement des anomalies pour démontrer le travail de nettoyage.

Les anomalies attendues sont :

```text
doublons de lignes
clés primaires dupliquées
valeurs manquantes
emails invalides
dates invalides
statuts non autorisés
plateformes non normalisées
montants incohérents
quantités négatives
relations invalides
textes de commentaires vides
données de paiement incomplètes
```

Ces anomalies ne sont pas des erreurs du projet. Elles servent à démontrer la capacité à contrôler, nettoyer et fiabiliser les données.

## 9. Exploitation des résultats

Les résultats de cette analyse sont utilisés dans l’étape suivante :

```text
src/data_processing/clean_and_standardize_data.py
```

Le nettoyage s’appuie sur les anomalies détectées pour :

```text
supprimer les doublons
normaliser les formats
corriger certaines valeurs
exclure les lignes non exploitables
recalculer les montants
standardiser les statuts
homogénéiser les plateformes
contrôler les relations entre tables
```

## 10. Lien avec les documents précédents

Ce document complète les documents de collecte :

```text
docs/01_sources_and_collection/06_collecte_depuis_fichiers.md
docs/01_sources_and_collection/07_collecte_depuis_api.md
docs/01_sources_and_collection/08_collecte_depuis_scraping.md
docs/01_sources_and_collection/09_collecte_depuis_base_donnees.md
docs/01_sources_and_collection/10_collecte_depuis_bigdata.md
```

Il fait aussi le lien avec le document suivant :

```text
docs/02_quality_and_processing/12_nettoyage_normalisation_donnees.md
```

## 11. Commande d’exécution

La commande d’exécution est :

```bash
python src/data_processing/analyze_extracted_data_quality.py
```

Le script doit être lancé depuis la racine du projet.

## 12. Résultat attendu

Après exécution, les rapports doivent être présents dans :

```text
data/interim/
```

Les fichiers attendus sont :

```text
extracted_quality_file_report.csv
extracted_quality_column_report.csv
extracted_quality_business_rules_report.csv
extracted_quality_summary.csv
```

Le script doit se terminer sans erreur bloquante.

## 13. Validation

L’étape est validée si :

```text
les fichiers extraits sont bien analysés
les rapports qualité sont générés
les anomalies sont identifiées
les erreurs critiques sont visibles
les résultats peuvent être utilisés pour le nettoyage
```

## 14. Conclusion

L’analyse qualité des données extraites permet de contrôler les données collectées avant leur nettoyage.

Elle fournit une vision précise des anomalies restantes après extraction multi-sources.

Cette étape sécurise le passage vers le nettoyage, la normalisation et l’agrégation finale du dataset IA.