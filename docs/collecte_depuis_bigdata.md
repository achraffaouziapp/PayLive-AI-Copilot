# Collecte depuis une source Big Data — Bloc 1

## 1. Objectif

Cette étape a pour objectif d’automatiser l’extraction de données depuis une source de type Big Data.

Dans le cadre du projet **PayLive AI Copilot**, cette source représente des logs d’événements générés pendant les sessions de live shopping.

Les événements simulés permettent de reproduire un contexte proche d’un système de logs ou d’un data lake, dans lequel les données sont stockées au format Parquet et exploitées avec des requêtes Spark SQL.

## 2. Source utilisée

La source utilisée est le fichier brut :

`data/raw/live_events_raw.csv`

Ce fichier contient des événements simulés liés aux lives :

- commentaire envoyé ;
- panier ouvert ;
- clic sur paiement ;
- paiement réussi ;
- erreur API ;
- produit consulté ;
- événement invalide volontairement injecté.

Afin de simuler une source Big Data, le fichier brut est transformé en source Parquet partitionnée dans :

`data/raw/bigdata/live_events_parquet`

Chaque dossier de cette source correspond à une partition par date d’événement, par exemple :

```text
event_date_partition=2026-01-01
event_date_partition=2026-01-02
event_date_partition=invalid_date
```

Cette organisation reproduit une structure courante de data lake.

## 3. Script utilisé

Le script utilisé est :

`src/data_collection/collect_from_bigdata.py`

## 4. Technologies utilisées

Les technologies utilisées sont :

- Python ;
- Pandas ;
- PyArrow ;
- PySpark ;
- Spark SQL ;
- Parquet.

PyArrow est utilisé pour créer et lire physiquement la source Parquet en local.

PySpark est utilisé pour charger les données dans un DataFrame Spark, créer une vue temporaire et exécuter les requêtes Spark SQL d’extraction et d’agrégation.

## 5. Adaptation technique pour Windows

Pendant l’exécution locale sous Windows, plusieurs contraintes techniques ont été rencontrées :

- Spark nécessite Java pour fonctionner ;
- la variable `JAVA_HOME` doit être configurée ;
- Spark peut afficher un warning lié à `winutils.exe` et `HADOOP_HOME` ;
- Spark peut rencontrer des erreurs avec l’accès direct aux fichiers Parquet sous Windows ;
- Spark peut utiliser le mauvais exécutable Python si un environnement virtuel est utilisé.

Pour rendre le script exécutable dans un environnement Windows avec un venv Python, les adaptations suivantes ont été réalisées :

- installation d’un JDK Java ;
- configuration de `JAVA_HOME` ;
- forçage de l’exécutable Python du venv via `PYSPARK_PYTHON` et `PYSPARK_DRIVER_PYTHON` ;
- utilisation de `sys.executable` pour garantir que Spark utilise le Python de `.venv` ;
- passage de Spark en mode local avec `local[1]` pour éviter les problèmes de workers multiples sous Windows ;
- création du Parquet avec Pandas et PyArrow au lieu de l’écriture directe avec Spark ;
- lecture du Parquet avec Pandas/PyArrow, puis conversion en DataFrame Spark ;
- conservation de Spark SQL pour les requêtes d’extraction.

Cette adaptation permet de conserver l’objectif pédagogique de l’étape Big Data tout en évitant les blocages liés à Hadoop NativeIO sous Windows.

## 6. Fonctionnement général du script

Le script réalise les actions suivantes :

1. vérification de la présence du fichier brut `live_events_raw.csv` ;
2. lecture des événements bruts ;
3. simulation d’un volume plus important grâce à un multiplicateur ;
4. ajout de colonnes techniques :
   - `source_event_id` ;
   - `simulation_copy_index` ;
   - `parsed_event_timestamp` ;
   - `event_date` ;
   - `event_hour` ;
   - `event_date_partition` ;
5. création d’une source Parquet partitionnée ;
6. lecture de la source Parquet avec PyArrow ;
7. conversion des données en DataFrame Spark ;
8. création d’une vue temporaire Spark SQL ;
9. exécution de requêtes Spark SQL ;
10. sauvegarde des résultats d’extraction ;
11. génération des rapports techniques ;
12. journalisation de l’exécution.

## 7. Données collectées

Les données collectées représentent des événements de live shopping.

Les principales colonnes sont :

- `event_id` ;
- `source_event_id` ;
- `live_id` ;
- `customer_id` ;
- `event_type` ;
- `event_timestamp` ;
- `parsed_event_timestamp` ;
- `event_date` ;
- `event_hour` ;
- `event_value` ;
- `source_system` ;
- `simulation_copy_index` ;
- `event_date_partition`.

## 8. Requêtes Spark SQL exécutées

Les requêtes Spark SQL sont documentées dans :

`sql/05_bigdata_extraction_queries.sql`

Elles permettent de produire plusieurs extractions.

### 8.1. Événements par live

Fichier généré :

`data/interim/bigdata_extracts/events_by_live_extract.csv`

Cette requête calcule, pour chaque live :

- le nombre total d’événements ;
- le nombre de clients uniques ;
- le nombre de commentaires ;
- le nombre d’ouvertures de panier ;
- le nombre de clics paiement ;
- le nombre de paiements réussis ;
- le nombre d’erreurs API.

### 8.2. Funnel paiement par live

Fichier généré :

`data/interim/bigdata_extracts/payment_funnel_by_live_extract.csv`

Cette requête calcule, pour chaque live :

- le nombre d’ouvertures de panier ;
- le nombre de clics paiement ;
- le nombre de paiements réussis ;
- le ratio de réussite du paiement.

### 8.3. Erreurs API par live

Fichier généré :

`data/interim/bigdata_extracts/api_errors_by_live_extract.csv`

Cette requête extrait et agrège les erreurs API par live et par système source.

### 8.4. Activité horaire

Fichier généré :

`data/interim/bigdata_extracts/hourly_activity_extract.csv`

Cette requête calcule le volume d’événements par :

- date ;
- heure ;
- type d’événement.

### 8.5. Événements invalides

Fichier généré :

`data/interim/bigdata_extracts/invalid_events_extract_extract.csv`

Cette requête identifie les événements présentant des anomalies :

- `live_id` manquant ;
- timestamp manquant ;
- timestamp invalide ;
- type d’événement non reconnu.

## 9. Sorties générées

L’exécution du script génère les éléments suivants :

```text
data/raw/bigdata/live_events_parquet/
data/interim/bigdata_extracts/events_by_live_extract.csv
data/interim/bigdata_extracts/payment_funnel_by_live_extract.csv
data/interim/bigdata_extracts/api_errors_by_live_extract.csv
data/interim/bigdata_extracts/hourly_activity_extract.csv
data/interim/bigdata_extracts/invalid_events_extract_extract.csv
data/interim/bigdata_extraction_manifest.csv
data/interim/bigdata_extraction_schema_report.csv
data/interim/bigdata_source_profile_report.csv
data/interim/bigdata_extraction_query_report.csv
data/interim/bigdata_parquet_creation_report.csv
data/interim/bigdata_extraction_errors.csv
sql/05_bigdata_extraction_queries.sql
logs/collect_from_bigdata.log
```

## 10. Rapports générés

### 10.1. Manifeste d’extraction

Fichier :

`data/interim/bigdata_extraction_manifest.csv`

Il contient :

- l’identifiant du batch d’extraction ;
- le nom de la source ;
- le type de source ;
- le moteur de traitement utilisé ;
- le chemin du fichier brut ;
- le chemin de la source Parquet ;
- le fichier contenant les requêtes SQL ;
- le statut d’exécution ;
- le nombre de requêtes exécutées ;
- le nombre de requêtes réussies.

### 10.2. Rapport de schéma

Fichier :

`data/interim/bigdata_extraction_schema_report.csv`

Il décrit les colonnes du DataFrame Spark :

- nom de colonne ;
- type Spark ;
- caractère nullable.

### 10.3. Rapport de profil de source

Fichier :

`data/interim/bigdata_source_profile_report.csv`

Il fournit une synthèse de la source :

- nombre total de lignes ;
- nombre de lives distincts ;
- nombre de clients distincts ;
- nombre de types d’événements ;
- nombre de timestamps invalides.

### 10.4. Rapport d’exécution des requêtes

Fichier :

`data/interim/bigdata_extraction_query_report.csv`

Il indique, pour chaque requête :

- son nom ;
- son statut ;
- le nombre de lignes retournées ;
- le nombre de colonnes ;
- le chemin du fichier de sortie ;
- le hash de la requête exécutée.

### 10.5. Rapport de création Parquet

Fichier :

`data/interim/bigdata_parquet_creation_report.csv`

Il documente la création de la source Parquet :

- fichier source utilisé ;
- dossier Parquet généré ;
- multiplicateur de simulation ;
- nombre de lignes ;
- nombre de colonnes ;
- colonne de partition ;
- statut de création.

### 10.6. Rapport d’erreurs

Fichier :

`data/interim/bigdata_extraction_errors.csv`

Il contient les erreurs éventuelles rencontrées pendant l’exécution.

Dans l’exécution validée, les requêtes ont toutes terminé avec le statut `success`.

## 11. Résultat d’exécution

L’exécution finale du script a produit le résultat suivant :

```text
Big data-based data collection completed successfully.
Manifest status:
success    1
Query status summary:
success    5
```

Cela confirme que :

- la source Parquet a bien été créée ;
- la session Spark a bien démarré ;
- les données ont été chargées dans Spark ;
- les requêtes Spark SQL ont été exécutées ;
- les cinq extractions Big Data ont réussi ;
- les rapports ont été générés.

## 12. Warnings observés

Pendant l’exécution sous Windows, certains warnings peuvent apparaître :

```text
Did not find winutils.exe
```

Ce warning est lié à l’environnement Windows et à Hadoop. Il n’est pas bloquant dans cette version du script, car l’accès physique aux fichiers Parquet est géré avec PyArrow.

Un autre warning peut apparaître :

```text
Stage contains a task of very large size
```

Ce warning est lié au chargement local d’un dataset simulé dans Spark. Il n’empêche pas l’exécution des requêtes et reste acceptable dans le cadre d’un environnement local de développement.

Un message lié à l’exécutable Python peut aussi apparaître au démarrage de Spark :

```text
Missing Python executable
```

Dans l’exécution validée, ce message n’a pas empêché Spark d’exécuter les requêtes. Pour limiter ce problème, le script force l’utilisation du Python de l’environnement virtuel avec `sys.executable`, `PYSPARK_PYTHON` et `PYSPARK_DRIVER_PYTHON`.

## 13. Justification

Cette étape permet de démontrer la capacité à exploiter une source de type Big Data.

Elle couvre notamment :

- la création d’une source Parquet partitionnée ;
- la manipulation de logs d’événements ;
- la préparation d’un dataset volumineux simulé ;
- l’utilisation de Spark SQL ;
- l’écriture de requêtes d’agrégation ;
- l’extraction d’indicateurs par live ;
- l’identification d’événements invalides ;
- la génération de rapports techniques.

Cette extraction complète les autres sources de collecte du Bloc 1 :

- fichiers CSV ;
- API REST ;
- scraping web ;
- base SQL ;
- source Big Data.

## 14. Limites

La source Big Data est simulée localement.

Elle ne correspond pas à un véritable cluster distribué, à un système Hive, HDFS ou S3.

Cependant, l’utilisation de fichiers Parquet partitionnés, d’un volume simulé de logs et de Spark SQL permet de reproduire une logique professionnelle proche d’un data lake.

Cette approche est adaptée au contexte du dossier professionnel, car elle démontre les compétences techniques attendues sans dépendre d’une infrastructure Big Data réelle.

## 15. Conclusion

La collecte depuis une source Big Data est validée.

Le projet dispose désormais d’une extraction multi-sources complète :

- fichiers CSV ;
- API REST ;
- scraping web ;
- base SQL ;
- source Big Data simulée.

Cette étape finalise la phase de collecte et d’extraction des données avant le passage au nettoyage, à la normalisation et à l’agrégation.