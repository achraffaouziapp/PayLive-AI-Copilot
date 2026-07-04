# Contrôle qualité de la base de données PostgreSQL — Bloc 1

## 1. Objectif

Cette étape a pour objectif de contrôler la qualité des données après leur import dans PostgreSQL.

Après la création de la base et l’import des fichiers préparés, il est nécessaire de vérifier que les données stockées sont cohérentes, complètes et exploitables.

Le contrôle qualité en base permet de vérifier :

```text
présence des tables
nombre de lignes importées
présence des clés primaires
absence de doublons sur les clés primaires
intégrité des clés étrangères
respect des valeurs catégorielles autorisées
absence de valeurs numériques négatives
présence du dataset final IA
statut du dernier import
```

## 2. Script utilisé

Le script utilisé est :

```text
src/database/check_database_quality.py
```

Il se connecte à PostgreSQL et génère plusieurs rapports dans :

```text
data/processed/
```

## 3. Position dans le pipeline

Cette étape intervient après :

```text
1. Collecte multi-sources
2. Analyse qualité des données extraites
3. Nettoyage et normalisation
4. Agrégation finale du dataset IA
5. Modélisation de la base
6. Création PostgreSQL
7. Import des données préparées
```

Elle prépare les étapes suivantes :

```text
8. Contrôle qualité en base
9. Documentation RGPD
10. Mise à disposition via API REST
```

## 4. Base de données contrôlée

La base contrôlée est :

```text
paylive_ai_copilot
```

Elle est exécutée avec Docker dans le conteneur :

```text
paylive_postgres
```

Paramètres de connexion utilisés :

```text
Host: localhost
Port: 5433
Database: paylive_ai_copilot
User: postgres
Password: postgres
```

Ces paramètres sont lus depuis le fichier :

```text
.env
```

## 5. Tables contrôlées

Le script contrôle les tables des schémas suivants :

```text
core
analytics
audit
```

## 5.1. Tables du schéma `core`

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

## 5.2. Table du schéma `analytics`

```text
analytics.dataset_final_live_sales
```

Cette table contient le dataset final agrégé prêt pour la suite IA.

## 5.3. Tables du schéma `audit`

```text
audit.import_batches
audit.import_logs
```

Ces tables contiennent les traces techniques des imports.

## 6. Rapports générés

Le script génère quatre rapports :

```text
data/processed/database_quality_table_report.csv
data/processed/database_quality_relationship_report.csv
data/processed/database_quality_business_report.csv
data/processed/database_quality_summary.csv
```

Un fichier de logs est également généré :

```text
logs/check_database_quality.log
```

## 7. Rapport des tables

Fichier généré :

```text
data/processed/database_quality_table_report.csv
```

Ce rapport contient une ligne par table contrôlée.

Colonnes principales :

```text
checked_at
schema_name
table_name
table_full_name
table_exists
row_count
column_count
primary_key_columns
missing_primary_key_rows
duplicate_primary_key_values
status
message
```

Ce rapport permet de vérifier :

```text
si la table existe
si la table contient des lignes
combien de colonnes elle possède
quelle est sa clé primaire
si des clés primaires sont manquantes
si des clés primaires sont dupliquées
```

## 8. Rapport d’intégrité relationnelle

Fichier généré :

```text
data/processed/database_quality_relationship_report.csv
```

Ce rapport contrôle les clés étrangères définies dans PostgreSQL.

Colonnes principales :

```text
constraint_name
source_table
source_column
target_table
target_column
orphan_rows
status
message
```

Un `orphan_rows` égal à zéro signifie que les références sont cohérentes.

Exemple :

```text
core.live_sessions.seller_id doit exister dans core.sellers.seller_id
core.carts.customer_id doit exister dans core.customers.customer_id
core.payments.order_id doit exister dans core.orders.order_id
```

## 9. Rapport des règles métier

Fichier généré :

```text
data/processed/database_quality_business_report.csv
```

Ce rapport vérifie des règles métier simples.

Contrôles effectués :

```text
valeurs catégorielles autorisées
valeurs numériques non négatives
ratios compris entre 0 et 1
présence du dataset final IA
cohérence du nombre de lignes du dataset final
statut du dernier import
```

## 10. Contrôle des valeurs autorisées

Le script vérifie que certaines colonnes ne contiennent que des valeurs autorisées.

Exemples de plateformes autorisées :

```text
tiktok
instagram
facebook_live
youtube_live
other
```

Exemples de statuts de paiement autorisés :

```text
pending
succeeded
failed
cancelled
refunded
```

Exemples de types d’événements autorisés :

```text
comment_sent
cart_opened
payment_clicked
payment_succeeded
api_error
product_viewed
```

## 11. Contrôle des valeurs numériques

Le script vérifie que les valeurs numériques importantes ne sont pas négatives.

Exemples :

```text
unit_price
stock_quantity
peak_viewers
total_amount
line_total
order_amount
payment_amount
total_revenue
total_events
```

Les valeurs négatives sur ces colonnes indiqueraient une incohérence.

## 12. Contrôle des ratios

Le script vérifie que certains ratios du dataset final sont compris entre 0 et 1.

Ratios contrôlés :

```text
purchase_intent_rate
cart_abandonment_rate
payment_success_rate
conversion_rate
```

Ces ratios doivent rester dans l’intervalle :

```text
0 <= ratio <= 1
```

## 13. Contrôle du dataset final IA

Le script contrôle la table :

```text
analytics.dataset_final_live_sales
```

Il vérifie notamment :

```text
présence de la table
nombre de lignes
cohérence avec core.live_sessions
statut final du dataset
absence de valeurs négatives sur le chiffre d’affaires
```

Le statut attendu est :

```text
ready_for_ai
```

## 14. Contrôle du dernier import

Le script vérifie le dernier import enregistré dans :

```text
audit.import_batches
```

Le statut attendu est :

```text
success
```

Si le dernier import a un statut différent, le rapport indique une anomalie.

## 15. Rapport de synthèse

Fichier généré :

```text
data/processed/database_quality_summary.csv
```

Ce rapport synthétise le résultat global.

Métriques principales :

```text
checked_at
global_status
tables_checked
failed_tables
warning_tables
relationships_checked
failed_relationships
business_rules_checked
failed_business_rules
total_rows_in_checked_tables
```

Le statut global peut être :

```text
success
warning
failed
```

## 16. Commande d’exécution

Avant d’exécuter le script, vérifier que Docker est lancé :

```bash
docker ps
```

Les conteneurs attendus sont :

```text
paylive_postgres
paylive_pgadmin
```

Puis lancer :

```bash
python src/database/check_database_quality.py
```

## 17. Résultat attendu

Le terminal doit afficher :

```text
Database quality checks completed.
Table report: .../data/processed/database_quality_table_report.csv
Relationship report: .../data/processed/database_quality_relationship_report.csv
Business report: .../data/processed/database_quality_business_report.csv
Summary report: .../data/processed/database_quality_summary.csv
```

Le statut global attendu dans le rapport de synthèse est :

```text
success
```

ou éventuellement :

```text
warning
```

Un statut `warning` peut apparaître si certaines tables sont vides ou si certains lives n’ont pas de revenu. Cela n’est pas forcément bloquant selon les données simulées.

## 18. Vérifications dans pgAdmin

Les résultats peuvent aussi être vérifiés dans pgAdmin :

```text
Servers
  -> PayLive PostgreSQL
    -> Databases
      -> paylive_ai_copilot
        -> Schemas
          -> core
          -> Tables
```

Il est possible d’ouvrir les tables avec :

```text
View/Edit Data -> All Rows
```

Tables utiles à vérifier :

```text
core.sellers
core.live_sessions
analytics.dataset_final_live_sales
audit.import_batches
audit.import_logs
```

## 19. Gestion des erreurs

Si le script échoue, vérifier :

```text
logs/check_database_quality.log
```

Puis vérifier :

```text
data/processed/database_quality_summary.csv
```

Causes possibles :

```text
PostgreSQL non démarré
mauvais port dans .env
base paylive_ai_copilot absente
tables non créées
données non importées
contraintes SQL non respectées
dernier import échoué
```

## 20. Importance pour le projet

Cette étape montre que la base de données n’est pas seulement créée, mais aussi contrôlée.

Elle permet de prouver :

```text
la présence des données en base
la cohérence des relations
la validité des principales règles métier
la disponibilité du dataset final IA
la traçabilité de l’import
```

## 21. Lien avec la suite

Après cette étape, la base PostgreSQL est prête pour :

```text
documentation RGPD
mise à disposition via API REST
requêtes analytiques
futurs traitements IA
```

L’étape suivante sera :

```text
docs/18_registre_rgpd.md
```

Puis la création de l’API REST.

## 22. Conclusion

Le contrôle qualité PostgreSQL permet de valider la cohérence des données importées.

Il génère des rapports exploitables pour le dossier professionnel et confirme que la base `paylive_ai_copilot` est prête pour les étapes suivantes du projet.