# Création de la base de données PostgreSQL — Bloc 1

## 1. Objectif

Cette étape a pour objectif de créer techniquement la base de données PostgreSQL du projet **PayLive AI Copilot**.

Après la modélisation de la base de données, les scripts SQL ont été créés afin de transformer le modèle logique et physique en une base relationnelle fonctionnelle.

La base créée permet de stocker :

- les données métiers nettoyées ;
- le dataset final agrégé pour l’IA ;
- les logs techniques d’import ;
- les futures données exposées par l’API REST.

La base finale s’appelle :

```text
paylive_ai_copilot
```

## 2. Position dans le pipeline

La création de la base intervient après :

```text
1. Collecte et extraction des données
2. Analyse qualité
3. Nettoyage et normalisation
4. Agrégation finale du dataset IA
5. Modélisation de la base de données
```

Elle prépare les étapes suivantes :

```text
6. Création technique de la base PostgreSQL
7. Import des données préparées
8. Contrôle qualité en base
9. Mise à disposition via API REST
```

## 3. Choix technique

Le SGBD utilisé est :

```text
PostgreSQL
```

La base est lancée avec Docker afin de rendre l’environnement reproductible.

Deux services Docker sont utilisés :

```text
postgres
pgadmin
```

Le service `postgres` héberge la base de données.

Le service `pgadmin` permet d’administrer visuellement PostgreSQL depuis un navigateur.

## 4. Fichier Docker Compose

Le fichier utilisé est :

```text
docker-compose.yml
```

Il définit deux conteneurs :

```text
paylive_postgres
paylive_pgadmin
```

## 4.1. Service PostgreSQL

Le service PostgreSQL utilise l’image :

```text
postgres:16
```

Configuration utilisée :

```yaml
postgres:
  image: postgres:16
  container_name: paylive_postgres
  restart: unless-stopped
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    POSTGRES_DB: postgres
  ports:
    - "5433:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

Le port local utilisé est :

```text
5433
```

Ce choix permet d’éviter un conflit avec un éventuel PostgreSQL déjà installé localement sur le port `5432`.

## 4.2. Service pgAdmin

Le service pgAdmin utilise l’image :

```text
dpage/pgadmin4:latest
```

Configuration utilisée :

```yaml
pgadmin:
  image: dpage/pgadmin4:latest
  container_name: paylive_pgadmin
  restart: unless-stopped
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@paylive.com
    PGADMIN_DEFAULT_PASSWORD: admin123
  ports:
    - "5050:80"
  depends_on:
    - postgres
```

pgAdmin est accessible sur :

```text
http://localhost:5050
```

Identifiants utilisés :

```text
Email: admin@paylive.com
Password: admin123
```

## 5. Problème rencontré avec pgAdmin

Lors du premier lancement, pgAdmin ne démarrait pas.

Les logs indiquaient que l’adresse suivante était refusée :

```text
admin@paylive.local
```

Erreur observée :

```text
The part after the @-sign is a special-use or reserved name that cannot be used with email.
'admin@paylive.local' does not appear to be a valid email address.
```

La correction a consisté à remplacer l’adresse par :

```text
admin@paylive.com
```

Puis le conteneur pgAdmin a été recréé.

Commandes utilisées :

```bash
docker rm -f paylive_pgadmin
docker compose up -d pgadmin
```

Après correction, pgAdmin a démarré correctement.

## 6. Lancement des conteneurs Docker

Les conteneurs sont lancés avec la commande :

```bash
docker compose up -d
```

La vérification est réalisée avec :

```bash
docker ps
```

Les conteneurs attendus sont :

```text
paylive_postgres
paylive_pgadmin
```

## 7. Connexion à PostgreSQL depuis pgAdmin

Dans pgAdmin, un serveur a été ajouté avec les paramètres suivants.

Onglet `General` :

```text
Name: PayLive PostgreSQL
```

Onglet `Connection` :

```text
Host name/address: postgres
Port: 5432
Maintenance database: postgres
Username: postgres
Password: postgres
```

Le host utilisé est :

```text
postgres
```

Ce choix est nécessaire car pgAdmin et PostgreSQL sont dans le même réseau Docker.

Depuis Windows, PostgreSQL est accessible via :

```text
localhost:5433
```

Depuis pgAdmin dans Docker, PostgreSQL est accessible via :

```text
postgres:5432
```

## 8. Scripts SQL créés

Les scripts SQL créés sont :

```text
sql/01_create_database.sql
sql/02_create_schemas.sql
sql/03_create_tables.sql
sql/04_create_indexes.sql
```

Ces scripts sont exécutés dans un ordre précis.

## 9. Script `01_create_database.sql`

Le script :

```text
sql/01_create_database.sql
```

permet de créer la base :

```text
paylive_ai_copilot
```

Il doit être exécuté depuis la base par défaut :

```text
postgres
```

Commande d’exécution :

```bash
docker cp sql/01_create_database.sql paylive_postgres:/tmp/01_create_database.sql
docker exec -it paylive_postgres psql -U postgres -d postgres -f /tmp/01_create_database.sql
```

Vérification :

```bash
docker exec -it paylive_postgres psql -U postgres -l
```

La base attendue doit apparaître dans la liste :

```text
paylive_ai_copilot
```

## 10. Script `02_create_schemas.sql`

Le script :

```text
sql/02_create_schemas.sql
```

permet de créer les schémas PostgreSQL suivants :

```text
core
analytics
audit
```

Commande d’exécution :

```bash
docker cp sql/02_create_schemas.sql paylive_postgres:/tmp/02_create_schemas.sql
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/02_create_schemas.sql
```

Vérification :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "\dn"
```

Schémas attendus :

```text
analytics
audit
core
public
```

## 11. Rôle des schémas

## 11.1. Schéma `core`

Le schéma `core` contient les tables métiers nettoyées :

```text
core.sellers
core.customers
core.products
core.live_sessions
core.live_products
core.live_comments
core.carts
core.cart_items
core.orders
core.payments
core.stock_movements
core.live_events
```

Ces tables correspondent aux fichiers nettoyés dans :

```text
data/processed/
```

## 11.2. Schéma `analytics`

Le schéma `analytics` contient le dataset final agrégé :

```text
analytics.dataset_final_live_sales
```

Cette table correspond au fichier :

```text
data/processed/dataset_final_live_sales.csv
```

Elle servira à la suite IA du projet.

## 11.3. Schéma `audit`

Le schéma `audit` contient les tables techniques d’import :

```text
audit.import_batches
audit.import_logs
```

Ces tables servent à tracer les imports CSV vers PostgreSQL.

## 12. Script `03_create_tables.sql`

Le script :

```text
sql/03_create_tables.sql
```

permet de créer toutes les tables de la base.

Commande d’exécution :

```bash
docker cp sql/03_create_tables.sql paylive_postgres:/tmp/03_create_tables.sql
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/03_create_tables.sql
```

## 12.1. Tables du schéma `core`

Les tables créées dans `core` sont :

```text
core.sellers
core.customers
core.products
core.live_sessions
core.live_products
core.live_comments
core.carts
core.cart_items
core.orders
core.payments
core.stock_movements
core.live_events
```

Ces tables contiennent les données métiers nettoyées.

Elles possèdent :

- des clés primaires ;
- des clés étrangères ;
- des contraintes de validation ;
- des contraintes de cohérence métier ;
- des commentaires SQL.

## 12.2. Table du schéma `analytics`

La table créée dans `analytics` est :

```text
analytics.dataset_final_live_sales
```

Elle contient une ligne par session live.

Elle regroupe les indicateurs calculés pendant l’agrégation finale :

```text
total_comments
purchase_intent_comments
total_carts
paid_carts
total_orders
total_revenue
payment_success_rate
conversion_rate
revenue_per_viewer
top_product_category
api_error_events
```

## 12.3. Tables du schéma `audit`

Les tables créées dans `audit` sont :

```text
audit.import_batches
audit.import_logs
```

Elles serviront à stocker les informations techniques de chaque import.

## 13. Vérification des tables

Pour vérifier les tables du schéma `core` :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "\dt core.*"
```

Pour vérifier les tables du schéma `analytics` :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "\dt analytics.*"
```

Pour vérifier les tables du schéma `audit` :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "\dt audit.*"
```

## 14. Contraintes principales créées

Les tables contiennent plusieurs types de contraintes.

## 14.1. Clés primaires

Chaque table métier possède une clé primaire :

```text
seller_id
customer_id
product_id
live_id
live_product_id
comment_id
cart_id
cart_item_id
order_id
payment_id
stock_movement_id
event_id
```

La table analytique possède également une clé primaire :

```text
live_id
```

## 14.2. Clés étrangères

Les principales clés étrangères sont :

```text
live_sessions.seller_id -> sellers.seller_id
live_products.live_id -> live_sessions.live_id
live_products.product_id -> products.product_id
live_comments.live_id -> live_sessions.live_id
live_comments.customer_id -> customers.customer_id
carts.live_id -> live_sessions.live_id
carts.customer_id -> customers.customer_id
cart_items.cart_id -> carts.cart_id
cart_items.product_id -> products.product_id
orders.cart_id -> carts.cart_id
orders.customer_id -> customers.customer_id
orders.seller_id -> sellers.seller_id
payments.order_id -> orders.order_id
stock_movements.product_id -> products.product_id
stock_movements.live_id -> live_sessions.live_id
live_events.live_id -> live_sessions.live_id
live_events.customer_id -> customers.customer_id
dataset_final_live_sales.live_id -> live_sessions.live_id
dataset_final_live_sales.seller_id -> sellers.seller_id
```

## 14.3. Contraintes CHECK

Des contraintes `CHECK` ont été ajoutées pour contrôler :

- les plateformes autorisées ;
- les statuts autorisés ;
- les devises autorisées ;
- les montants positifs ;
- les quantités positives ;
- les compteurs positifs ;
- le statut final du dataset analytique.

Exemple de valeurs autorisées pour les plateformes :

```text
tiktok
instagram
facebook_live
youtube_live
other
```

Exemple de statuts de paiement autorisés :

```text
pending
succeeded
failed
cancelled
refunded
```

## 15. Script `04_create_indexes.sql`

Le script :

```text
sql/04_create_indexes.sql
```

permet de créer les index PostgreSQL.

Commande d’exécution :

```bash
docker cp sql/04_create_indexes.sql paylive_postgres:/tmp/04_create_indexes.sql
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/04_create_indexes.sql
```

## 16. Rôle des index

Les index servent à optimiser :

- les jointures entre tables ;
- les filtres par vendeur ;
- les filtres par client ;
- les filtres par live ;
- les filtres par produit ;
- les filtres par plateforme ;
- les filtres par date ;
- les futures requêtes de l’API REST ;
- les requêtes analytiques sur le dataset final.

## 17. Exemples d’index créés

Index sur les lives :

```text
idx_live_sessions_seller_id
idx_live_sessions_platform
idx_live_sessions_actual_start_at
```

Index sur les commentaires :

```text
idx_live_comments_live_id
idx_live_comments_customer_id
idx_live_comments_intent
idx_live_comments_live_intent
```

Index sur les paniers :

```text
idx_carts_live_id
idx_carts_customer_id
idx_carts_cart_status
```

Index sur les commandes et paiements :

```text
idx_orders_cart_id
idx_orders_seller_id
idx_payments_order_id
idx_payments_payment_status
```

Index sur les événements :

```text
idx_live_events_live_id
idx_live_events_event_type
idx_live_events_event_timestamp
```

Index sur le dataset final :

```text
idx_dataset_final_live_sales_seller_id
idx_dataset_final_live_sales_platform
idx_dataset_final_live_sales_live_date
idx_dataset_final_live_sales_conversion_rate
```

## 18. Vérification des index

Pour vérifier les index du schéma `core` :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "\di core.*"
```

Pour vérifier les index du schéma `analytics` :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "\di analytics.*"
```

Pour vérifier les index du schéma `audit` :

```bash
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -c "\di audit.*"
```

## 19. Vérification dans pgAdmin

La vérification peut également être réalisée dans pgAdmin.

Dans l’interface :

```text
Servers
  -> PayLive PostgreSQL
    -> Databases
      -> paylive_ai_copilot
        -> Schemas
```

Les schémas attendus sont :

```text
core
analytics
audit
```

Dans chaque schéma, il est possible de vérifier :

```text
Tables
Indexes
Constraints
```

Cette vérification permet de confirmer que la structure PostgreSQL a bien été créée.

## 20. Ordre complet d’exécution

L’ordre complet des scripts est :

```bash
docker cp sql/01_create_database.sql paylive_postgres:/tmp/01_create_database.sql
docker exec -it paylive_postgres psql -U postgres -d postgres -f /tmp/01_create_database.sql

docker cp sql/02_create_schemas.sql paylive_postgres:/tmp/02_create_schemas.sql
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/02_create_schemas.sql

docker cp sql/03_create_tables.sql paylive_postgres:/tmp/03_create_tables.sql
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/03_create_tables.sql

docker cp sql/04_create_indexes.sql paylive_postgres:/tmp/04_create_indexes.sql
docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/04_create_indexes.sql
```

## 21. Commandes utiles Docker

Voir les conteneurs actifs :

```bash
docker ps
```

Voir tous les conteneurs :

```bash
docker ps -a
```

Voir les logs PostgreSQL :

```bash
docker logs paylive_postgres --tail 50
```

Voir les logs pgAdmin :

```bash
docker logs paylive_pgadmin --tail 50
```

Arrêter les conteneurs :

```bash
docker compose down
```

Relancer les conteneurs :

```bash
docker compose up -d
```

## 22. Résultat obtenu

À la fin de cette étape, l’environnement PostgreSQL est opérationnel.

La base suivante existe :

```text
paylive_ai_copilot
```

Les schémas suivants existent :

```text
core
analytics
audit
```

Les tables métiers, analytiques et techniques sont créées.

Les index nécessaires aux jointures, filtres et futures requêtes API sont également créés.

## 23. Importance pour le projet

Cette étape permet de passer de fichiers CSV préparés à une base relationnelle structurée.

Elle apporte :

- une organisation claire des données ;
- une séparation entre données métiers et données analytiques ;
- une meilleure intégrité grâce aux clés étrangères ;
- une validation des données grâce aux contraintes SQL ;
- une base exploitable par une API REST ;
- une base exploitable par les futurs traitements IA.

## 24. Limites

À cette étape, la base est créée mais les tables ne contiennent pas encore de données.

L’import sera réalisé dans l’étape suivante avec le script :

```text
src/database/import_processed_data.py
```

Ce script lira les fichiers présents dans :

```text
data/processed/
```

puis les insérera dans PostgreSQL dans le bon ordre.

## 25. Prochaine étape

La prochaine étape est l’import des données préparées dans PostgreSQL.

Fichier à créer :

```text
src/database/import_processed_data.py
```

Documentation associée prévue :

```text
docs/16_import_donnees_postgresql.md
```

## 26. Conclusion

La création de la base PostgreSQL permet de concrétiser la modélisation réalisée précédemment.

Les scripts SQL créés permettent de construire un environnement structuré et reproductible :

```text
01_create_database.sql
02_create_schemas.sql
03_create_tables.sql
04_create_indexes.sql
```

Cette base servira ensuite à importer les données nettoyées, à exposer les données via une API REST et à alimenter les futures étapes IA du projet PayLive AI Copilot.