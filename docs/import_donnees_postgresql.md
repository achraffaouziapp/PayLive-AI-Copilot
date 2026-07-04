# Import des données préparées dans PostgreSQL — Bloc 1

## 1. Objectif

Cette étape a pour objectif d’importer les données préparées du projet **PayLive AI Copilot** dans la base PostgreSQL finale.

Les données ont déjà été :

```text
collectées
extraites
analysées
nettoyées
normalisées
agrégées
```

Elles sont disponibles dans le dossier :

```text
data/processed/
```

L’objectif est maintenant de les charger dans la base :

```text
paylive_ai_copilot
```

## 2. Position dans le pipeline

Cette étape intervient après la création technique de la base PostgreSQL.

Le pipeline est donc :

```text
1. Collecte multi-sources
2. Analyse qualité
3. Nettoyage et normalisation
4. Agrégation finale du dataset IA
5. Modélisation de la base
6. Création PostgreSQL
7. Import des données préparées
8. Contrôle qualité en base
9. Mise à disposition via API REST
```

## 3. Script utilisé

Le script utilisé est :

```text
src/database/import_processed_data.py
```

Il importe les fichiers CSV nettoyés et agrégés dans PostgreSQL.

## 4. Base de données cible

La base cible est :

```text
paylive_ai_copilot
```

Elle est lancée avec Docker via le conteneur :

```text
paylive_postgres
```

La connexion depuis la machine locale se fait avec :

```text
Host: localhost
Port: 5433
Database: paylive_ai_copilot
User: postgres
Password: postgres
```

Le port `5433` correspond au port exposé dans `docker-compose.yml`.

## 5. Configuration `.env`

Le script lit les paramètres de connexion depuis le fichier :

```text
.env
```

Configuration utilisée :

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=paylive_ai_copilot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

Le fichier `.env.example` contient la même structure afin de documenter les variables nécessaires sans dépendre d’une configuration locale.

## 6. Dépendances Python

Le script utilise notamment :

```text
pandas
psycopg2-binary
python-dotenv
```

Ces dépendances doivent être présentes dans :

```text
requirements.txt
```

Installation :

```bash
pip install -r requirements.txt
```

## 7. Données importées

Le script importe les fichiers suivants :

```text
data/processed/sellers_clean.csv
data/processed/customers_clean.csv
data/processed/products_clean.csv
data/processed/live_sessions_clean.csv
data/processed/live_products_clean.csv
data/processed/live_comments_clean.csv
data/processed/carts_clean.csv
data/processed/cart_items_clean.csv
data/processed/orders_clean.csv
data/processed/payments_clean.csv
data/processed/stock_movements_clean.csv
data/processed/live_events_clean.csv
data/processed/dataset_final_live_sales.csv
```

## 8. Tables cibles

Les fichiers nettoyés sont importés dans le schéma :

```text
core
```

Correspondances :

```text
sellers_clean.csv          -> core.sellers
customers_clean.csv        -> core.customers
products_clean.csv         -> core.products
live_sessions_clean.csv    -> core.live_sessions
live_products_clean.csv    -> core.live_products
live_comments_clean.csv    -> core.live_comments
carts_clean.csv            -> core.carts
cart_items_clean.csv       -> core.cart_items
orders_clean.csv           -> core.orders
payments_clean.csv         -> core.payments
stock_movements_clean.csv  -> core.stock_movements
live_events_clean.csv      -> core.live_events
```

Le dataset final IA est importé dans le schéma :

```text
analytics
```

Correspondance :

```text
dataset_final_live_sales.csv -> analytics.dataset_final_live_sales
```

## 9. Tables d’audit

Le script écrit également dans les tables techniques :

```text
audit.import_batches
audit.import_logs
```

La table `audit.import_batches` contient une ligne par exécution globale d’import.

La table `audit.import_logs` contient une ligne par fichier importé.

Ces tables permettent de tracer :

```text
date d’import
fichier source
table cible
nombre de lignes lues
nombre de lignes insérées
statut de l’import
message d’erreur éventuel
```

## 10. Ordre d’import

L’ordre d’import respecte les dépendances entre tables.

Ordre utilisé :

```text
1. core.sellers
2. core.customers
3. core.products
4. core.live_sessions
5. core.live_products
6. core.live_comments
7. core.carts
8. core.cart_items
9. core.orders
10. core.payments
11. core.stock_movements
12. core.live_events
13. analytics.dataset_final_live_sales
```

Cet ordre permet de charger d’abord les tables référencées par des clés étrangères.

Exemple :

```text
core.live_sessions dépend de core.sellers
core.carts dépend de core.live_sessions et core.customers
core.orders dépend de core.carts, core.customers et core.sellers
core.payments dépend de core.orders
```

## 11. Nettoyage préalable des tables

Avant l’import, le script vide les tables cibles avec :

```text
TRUNCATE TABLE ... RESTART IDENTITY CASCADE
```

Les tables vidées sont les tables `core` et `analytics`.

Les tables `audit` ne sont pas vidées afin de conserver l’historique des imports.

Cette stratégie permet de relancer le script plusieurs fois sans dupliquer les données.

## 12. Méthode d’import utilisée

Le script utilise la commande PostgreSQL :

```text
COPY
```

Cette méthode est plus efficace qu’une insertion ligne par ligne.

Le script lit chaque CSV avec `pandas`, conserve les colonnes correspondant à la table cible, puis utilise `COPY` pour charger les données dans PostgreSQL.

Les valeurs vides sont importées comme `NULL`.

## 13. Gestion des colonnes

Pour chaque fichier, le script compare :

```text
colonnes du CSV
colonnes de la table PostgreSQL
```

Il conserve uniquement les colonnes présentes dans la table cible.

Le rapport d’import indique :

```text
table_columns_count
imported_columns_count
skipped_source_columns
missing_source_columns
```

Cela permet de vérifier que le fichier CSV correspond bien à la table PostgreSQL.

## 14. Rapports générés

Le script génère deux rapports CSV :

```text
data/processed/database_import_report.csv
data/processed/database_import_summary.csv
```

Il génère également un fichier de logs :

```text
logs/import_processed_data.log
```

## 15. Rapport détaillé d’import

Le fichier :

```text
data/processed/database_import_report.csv
```

contient une ligne par table importée.

Colonnes principales :

```text
import_batch_id
schema_name
table_name
table_full_name
source_file
source_file_exists
rows_read
rows_inserted
table_columns_count
imported_columns_count
skipped_source_columns
missing_source_columns
status
error_message
imported_at
```

Ce rapport permet d’identifier précisément les imports réussis ou échoués.

## 16. Rapport de synthèse

Le fichier :

```text
data/processed/database_import_summary.csv
```

contient une synthèse de l’import.

Métriques principales :

```text
import_batch_id
started_at
ended_at
status
total_tables
successful_tables
failed_tables
total_rows_read
total_rows_inserted
source_folder
```

Le statut global peut être :

```text
success
partial_success
failed
```

## 17. Logs techniques

Le fichier :

```text
logs/import_processed_data.log
```

contient les traces techniques de l’exécution.

Il permet de diagnostiquer les erreurs éventuelles :

```text
erreur de connexion
fichier manquant
table inexistante
contrainte SQL violée
erreur de type
erreur de clé étrangère
```

## 18. Commande d’exécution

Avant d’exécuter le script, vérifier que les conteneurs Docker sont actifs :

```bash
docker ps
```

Les conteneurs attendus sont :

```text
paylive_postgres
paylive_pgadmin
```

Ensuite, exécuter :

```bash
python src/database/import_processed_data.py
```

## 19. Résultat attendu

Le terminal doit afficher un résultat proche de :

```text
Processed data import into PostgreSQL completed.
Import report: .../data/processed/database_import_report.csv
Import summary: .../data/processed/database_import_summary.csv
Log file: .../logs/import_processed_data.log

Import summary:
metric               value
import_batch_id      IMPORT_...
status               success
total_tables         13
successful_tables    13
failed_tables        0
total_rows_read      ...
total_rows_inserted  ...
```

Le statut attendu est :

```text
success
```

## 20. Vérifications SQL

Vérifier le nombre de vendeurs importés :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "SELECT COUNT(*) FROM core.sellers;"
```

Vérifier le nombre de lives importés :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "SELECT COUNT(*) FROM core.live_sessions;"
```

Vérifier le dataset final :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "SELECT COUNT(*) FROM analytics.dataset_final_live_sales;"
```

Vérifier les logs d’import :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "SELECT schema_name, table_name, rows_inserted, status FROM audit.import_logs ORDER BY imported_at DESC LIMIT 20;"
```

## 21. Vérification dans pgAdmin

Dans pgAdmin :

```text
Servers
  -> PayLive PostgreSQL
    -> Databases
      -> paylive_ai_copilot
        -> Schemas
          -> core
          -> Tables
```

Ensuite :

```text
clic droit sur une table
View/Edit Data
All Rows
```

La même vérification peut être faite pour :

```text
analytics.dataset_final_live_sales
audit.import_batches
audit.import_logs
```

## 22. Gestion des erreurs

Si l’import échoue, consulter d’abord :

```text
data/processed/database_import_report.csv
```

Puis :

```text
logs/import_processed_data.log
```

Exemples d’erreurs possibles :

```text
PostgreSQL non démarré
mauvais port de connexion
base paylive_ai_copilot inexistante
schémas ou tables non créés
fichier CSV manquant
contrainte de clé étrangère non respectée
type de donnée incompatible
```

## 23. Importance pour le projet

Cette étape permet de passer de fichiers CSV à une base relationnelle exploitable.

Elle apporte :

```text
stockage structuré
intégrité référentielle
historique d’import
séparation core / analytics / audit
base prête pour l’API REST
base prête pour les requêtes analytiques
```

## 24. Lien avec la suite du projet

Après l’import, la prochaine étape sera de contrôler la qualité des données directement en base.

Le script prévu est :

```text
src/database/check_database_quality.py
```

Il vérifiera notamment :

```text
nombre de lignes par table
présence de clés primaires
intégrité référentielle
présence du dataset final
cohérence des indicateurs principaux
```

Ensuite, la base pourra être utilisée par l’API REST.

## 25. Conclusion

Le script `import_processed_data.py` permet d’importer automatiquement les données préparées du projet PayLive AI Copilot dans PostgreSQL.

Il charge les tables métiers dans `core`, le dataset final IA dans `analytics` et conserve les traces d’import dans `audit`.

Cette étape valide la mise en base des données préparées et prépare la future mise à disposition via API REST.