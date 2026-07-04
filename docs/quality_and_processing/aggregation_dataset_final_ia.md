# Agrégation finale du dataset IA — Bloc 1

## 1. Objectif

Cette étape a pour objectif de construire le dataset final du projet **PayLive AI Copilot**.

Après les étapes de collecte, d’extraction, d’analyse qualité, de nettoyage et de normalisation, les données sont encore réparties dans plusieurs fichiers métiers :

- vendeurs ;
- clients ;
- produits ;
- sessions live ;
- commentaires ;
- paniers ;
- commandes ;
- paiements ;
- événements live ;
- produits présentés pendant les lives.

L’objectif de cette étape est donc de regrouper ces données nettoyées dans un seul dataset analytique exploitable pour la suite du projet IA.

Le fichier final généré est :

```text
data/processed/dataset_final_live_sales.csv
```

Ce fichier contient une ligne par session live.

## 2. Script utilisé

Le script utilisé est :

```text
src/data_processing/build_final_ai_dataset.py
```

Il lit les fichiers nettoyés présents dans :

```text
data/processed/
```

Puis il génère le dataset final ainsi que plusieurs rapports techniques.

## 3. Position dans le pipeline de données

Le pipeline du Bloc 1 suit l’ordre suivant :

```text
1. Génération des données simulées
2. Extraction multi-sources
3. Analyse qualité des données extraites
4. Nettoyage et normalisation
5. Agrégation finale du dataset IA
6. Stockage en base de données
7. Mise à disposition via API REST
```

L’agrégation finale intervient donc après le nettoyage.

Elle transforme plusieurs tables propres en un dataset unique prêt pour l’analyse, la visualisation ou les futurs traitements IA.

## 4. Granularité du dataset final

La granularité du dataset final est :

```text
1 ligne = 1 session live
```

Chaque ligne représente un live TikTok, Instagram ou autre plateforme.

Le dataset final permet donc d’analyser la performance d’un live à partir de plusieurs familles d’indicateurs :

- informations du live ;
- informations du vendeur ;
- engagement des commentaires ;
- paniers ;
- commandes ;
- paiements ;
- produits présentés ;
- événements techniques et comportementaux ;
- ratios métier.

## 5. Sources utilisées

Le script utilise les fichiers nettoyés suivants :

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
```

Ces fichiers ont été produits par le script :

```text
src/data_processing/clean_and_standardize_data.py
```

Le dataset final ne travaille donc pas directement sur les données brutes, mais sur les données déjà nettoyées et normalisées.

## 6. Sorties générées

L’exécution du script génère les fichiers suivants :

```text
data/processed/dataset_final_live_sales.csv
data/processed/final_dataset_manifest.csv
data/processed/final_dataset_quality_report.csv
data/processed/final_dataset_aggregation_report.csv
logs/build_final_ai_dataset.log
```

## 7. Dataset final généré

Le fichier principal est :

```text
data/processed/dataset_final_live_sales.csv
```

Il contient une ligne par live.

Il regroupe des indicateurs issus de plusieurs sources nettoyées.

Exemple de colonnes finales :

```text
live_id
seller_id
shop_name
platform
live_date
peak_viewers
total_comments
purchase_intent_comments
total_carts
paid_carts
total_orders
total_revenue
payment_success_rate
conversion_rate
top_product_category
api_error_events
final_dataset_status
```

La colonne :

```text
final_dataset_status
```

contient la valeur :

```text
ready_for_ai
```

Cela indique que le dataset est prêt pour la suite du projet IA.

## 8. Construction du dataset de base

Le dataset final commence à partir de :

```text
live_sessions_clean.csv
```

Cette table sert de base car elle contient les sessions live.

Les colonnes principales conservées sont :

```text
live_id
seller_id
platform
live_title
live_status
live_date
peak_viewers
currency
```

La colonne `live_date` est calculée à partir de :

```text
actual_start_at
```

Si cette date est absente, le script utilise :

```text
scheduled_start_at
```

Ensuite, les informations du vendeur sont ajoutées depuis :

```text
sellers_clean.csv
```

Les colonnes ajoutées sont :

```text
shop_name
seller_country
main_platform
seller_status
```

Cette première étape permet d’obtenir une base avec une ligne par live et le contexte vendeur associé.

## 9. Agrégation des commentaires

Les commentaires sont agrégés depuis :

```text
live_comments_clean.csv
```

L’agrégation se fait par :

```text
live_id
```

Les indicateurs créés sont :

```text
total_comments
purchase_intent_comments
product_question_comments
payment_question_comments
shipping_question_comments
other_comments
unknown_intent_comments
unique_comment_customers
```

Ces indicateurs mesurent l’engagement des spectateurs pendant le live.

Ils permettent aussi de préparer la suite IA, notamment pour analyser les intentions d’achat dans les commentaires.

## 10. Agrégation des paniers

Les paniers sont agrégés depuis :

```text
carts_clean.csv
```

L’agrégation se fait par :

```text
live_id
```

Les indicateurs créés sont :

```text
total_carts
paid_carts
abandoned_carts
open_carts
cancelled_carts
unique_cart_customers
```

Ces indicateurs mesurent l’engagement commercial pendant le live.

Ils permettent de savoir combien de paniers ont été créés, payés, abandonnés ou annulés.

## 11. Agrégation des commandes

Les commandes sont agrégées depuis :

```text
orders_clean.csv
```

Une commande n’est pas directement reliée au live.

Elle est rattachée au live grâce au panier :

```text
orders.cart_id -> carts.cart_id -> carts.live_id
```

Les indicateurs créés sont :

```text
total_orders
paid_orders
confirmed_orders
pending_orders
cancelled_orders
refunded_orders
total_order_amount
average_order_amount
```

Ces indicateurs mesurent la performance commerciale du live en termes de commandes.

## 12. Agrégation des paiements

Les paiements sont agrégés depuis :

```text
payments_clean.csv
```

Un paiement est rattaché au live grâce au chemin suivant :

```text
payments.order_id -> orders.order_id -> orders.cart_id -> carts.cart_id -> carts.live_id
```

Les indicateurs créés sont :

```text
total_payments
successful_payments
failed_payments
pending_payments
cancelled_payments
refunded_payments
total_revenue
payment_success_rate
```

Le chiffre d’affaires du live est calculé uniquement à partir des paiements réussis.

La colonne utilisée est :

```text
total_revenue
```

Elle correspond à la somme des montants des paiements dont le statut est :

```text
succeeded
```

## 13. Agrégation des produits

Les produits présentés pendant les lives sont agrégés depuis :

```text
live_products_clean.csv
products_clean.csv
```

La jointure se fait sur :

```text
product_id
```

Les indicateurs créés sont :

```text
total_products_presented
total_initial_stock
total_remaining_stock
estimated_sold_quantity
average_live_product_price
top_product_category
```

La quantité estimée vendue est calculée avec la règle suivante :

```text
estimated_sold_quantity = total_initial_stock - total_remaining_stock
```

Si le résultat est négatif, il est remplacé par zéro.

La catégorie principale du live est déterminée à partir de la catégorie produit la plus fréquente.

## 14. Agrégation des événements live

Les événements live sont agrégés depuis :

```text
live_events_clean.csv
```

L’agrégation se fait par :

```text
live_id
```

Les indicateurs créés sont :

```text
total_events
comment_event_count
cart_opened_events
payment_clicked_events
payment_succeeded_events
api_error_events
product_view_events
unique_event_customers
```

Ces indicateurs apportent une dimension comportementale et technique.

Ils permettent d’analyser :

- l’activité des utilisateurs ;
- les ouvertures de paniers ;
- les clics paiement ;
- les paiements réussis ;
- les erreurs API ;
- les consultations produits.

## 15. Ratios métier calculés

Le script ajoute plusieurs ratios utiles pour l’analyse et la future partie IA.

### 15.1. Taux d’intention d’achat

```text
purchase_intent_rate = purchase_intent_comments / total_comments
```

Ce ratio mesure la proportion de commentaires exprimant une intention d’achat.

### 15.2. Taux d’abandon panier

```text
cart_abandonment_rate = abandoned_carts / total_carts
```

Ce ratio mesure la proportion de paniers abandonnés.

### 15.3. Ratio commentaires vers paniers

```text
comment_to_cart_rate = total_carts / total_comments
```

Ce ratio permet d’observer la capacité du live à transformer l’engagement en création de panier.

### 15.4. Taux de réussite paiement

```text
payment_success_rate = successful_payments / total_payments
```

Ce ratio mesure la fiabilité du tunnel de paiement.

### 15.5. Taux de conversion

```text
conversion_rate = paid_carts / peak_viewers
```

Ce ratio mesure la conversion approximative des spectateurs en paniers payés.

### 15.6. Revenu par spectateur

```text
revenue_per_viewer = total_revenue / peak_viewers
```

Ce ratio mesure la valeur moyenne générée par spectateur.

### 15.7. Revenu par commande

```text
revenue_per_order = total_revenue / total_orders
```

Ce ratio mesure le revenu moyen par commande.

## 16. Gestion des divisions par zéro

Le script utilise une fonction de division sécurisée.

Si le dénominateur est égal à zéro ou absent, le ratio prend la valeur :

```text
0
```

Cela évite les erreurs de calcul et garantit que le dataset final reste exploitable.

Exemples :

```text
total_comments = 0 -> purchase_intent_rate = 0
total_payments = 0 -> payment_success_rate = 0
peak_viewers = 0 -> conversion_rate = 0
```

## 17. Rapport d’agrégation

Le script génère un rapport détaillé :

```text
data/processed/final_dataset_aggregation_report.csv
```

Ce rapport décrit chaque étape d’agrégation.

Il contient notamment :

```text
aggregation_step
source_datasets
source_row_count
aggregation_level
created_indicators
business_purpose
```

Les étapes documentées sont :

```text
base_live_dataset
comments_aggregation
carts_aggregation
orders_aggregation
payments_aggregation
products_aggregation
events_aggregation
business_ratios
final_dataset
```

Ce rapport permet de justifier les choix d’agrégation et de montrer comment les indicateurs ont été construits.

## 18. Rapport qualité du dataset final

Le script génère également :

```text
data/processed/final_dataset_quality_report.csv
```

Ce rapport contient des contrôles sur le dataset final :

```text
row_count
column_count
total_cells
missing_cells
blank_cells
duplicate_live_id_count
lives_without_comments
lives_without_carts
lives_without_orders
lives_without_revenue
lives_with_zero_peak_viewers
negative_revenue_rows
dataset_status
```

Ces contrôles permettent de vérifier que le dataset final est cohérent avant de passer au stockage ou aux étapes IA.

## 19. Manifeste du dataset final

Le manifeste généré est :

```text
data/processed/final_dataset_manifest.csv
```

Il contient :

```text
generated_at
dataset_name
dataset_type
output_file
output_file_hash_sha256
row_count
column_count
granularity
source_files
quality_report
status
```

Le manifeste permet de tracer la génération du fichier final.

Il indique aussi le hash SHA256 du dataset final, ce qui permet de vérifier si le fichier a été modifié.

## 20. Fichier de logs

Le fichier de logs est :

```text
logs/build_final_ai_dataset.log
```

Il permet de tracer l’exécution technique du script.

Il contient notamment les informations de chargement des datasets nettoyés et la sauvegarde des sorties finales.

## 21. Commande d’exécution

Le script s’exécute depuis la racine du projet avec la commande suivante :

```bash
python src/data_processing/build_final_ai_dataset.py
```

## 22. Résultat attendu

Après exécution, le terminal doit afficher un message proche de :

```text
Final AI dataset aggregation completed successfully.
Final dataset: .../data/processed/dataset_final_live_sales.csv
Final manifest: .../data/processed/final_dataset_manifest.csv
Final quality report: .../data/processed/final_dataset_quality_report.csv
```

Cela confirme que :

- les datasets nettoyés ont été chargés ;
- les agrégations ont été réalisées ;
- les indicateurs ont été calculés ;
- les ratios métier ont été créés ;
- le dataset final a été sauvegardé ;
- le manifeste a été généré ;
- le rapport qualité a été généré ;
- le rapport d’agrégation a été généré.

## 23. Exemple de ligne du dataset final

Une ligne du dataset final peut représenter un live comme ceci :

```text
live_id: LIVE_001
seller_id: SELLER_003
shop_name: Boutique Nova
platform: tiktok
live_date: 2026-02-15
peak_viewers: 850
total_comments: 320
purchase_intent_comments: 74
total_carts: 45
paid_carts: 28
total_orders: 28
total_revenue: 1260.50
payment_success_rate: 0.82
conversion_rate: 0.0329
top_product_category: fashion
api_error_events: 3
final_dataset_status: ready_for_ai
```

Cette ligne résume la performance commerciale, comportementale et technique d’un live.

## 24. Intérêt pour la suite IA

Le dataset final est important pour le Bloc 2, car il pourra servir de base à différents travaux IA.

Exemples d’usages possibles :

```text
prédire la performance commerciale d’un live
identifier les lives à fort potentiel
détecter les facteurs qui influencent le taux de conversion
analyser l’impact des intentions d’achat sur le chiffre d’affaires
classer les lives selon leur performance
alimenter un tableau de bord intelligent
```

Le dataset contient déjà des variables explicatives exploitables :

```text
total_comments
purchase_intent_rate
total_carts
payment_success_rate
api_error_events
total_products_presented
average_live_product_price
peak_viewers
```

Il contient aussi des variables cibles potentielles :

```text
total_revenue
conversion_rate
revenue_per_viewer
paid_carts
```

## 25. Justification RGPD

Le dataset final est construit à partir de données simulées.

Aucune donnée réelle de PayLive n’est utilisée.

Le dataset final ne conserve pas les informations personnelles détaillées des clients.

Il travaille principalement au niveau agrégé par live.

Les identifiants encore présents sont des identifiants fictifs :

```text
live_id
seller_id
```

Les données personnelles comme les emails, numéros de téléphone ou commentaires détaillés ne sont pas nécessaires dans ce dataset final analytique.

Cette approche respecte le principe de minimisation des données.

## 26. Limites

Le dataset final est basé sur des données simulées.

Certaines règles sont simplifiées :

- le chiffre d’affaires est calculé uniquement à partir des paiements réussis ;
- la conversion est estimée avec les paniers payés et le pic de spectateurs ;
- la quantité vendue est estimée avec le stock initial et le stock restant ;
- la catégorie principale est basée sur la fréquence des catégories produits ;
- les données ne représentent pas l’activité réelle de PayLive.

Dans un projet réel, ces règles devraient être validées avec les équipes métier.

## 27. Contrôles à effectuer après génération

Après exécution du script, il faut vérifier la présence des fichiers suivants :

```text
data/processed/dataset_final_live_sales.csv
data/processed/final_dataset_manifest.csv
data/processed/final_dataset_quality_report.csv
data/processed/final_dataset_aggregation_report.csv
logs/build_final_ai_dataset.log
```

Il faut également ouvrir le fichier :

```text
data/processed/final_dataset_quality_report.csv
```

et vérifier notamment :

```text
duplicate_live_id_count = 0
negative_revenue_rows = 0
dataset_status = ready_for_ai
```

## 28. Versionnement Git

Après génération du dataset final et des rapports, les fichiers doivent être versionnés avec Git.

Commande recommandée :

```bash
git add .
git commit -m "Add final AI dataset aggregation documentation"
```

Si le dataset final est volumineux, il pourra être gardé localement ou géré avec une stratégie spécifique dans `.gitignore`.

## 29. Conclusion

Cette étape finalise la préparation du jeu de données exploitable pour le projet IA.

Elle transforme plusieurs datasets nettoyés en un dataset unique, structuré et documenté.

Le résultat principal est :

```text
data/processed/dataset_final_live_sales.csv
```

Ce fichier est prêt pour :

- le stockage en base de données ;
- l’exposition via API REST ;
- l’analyse métier ;
- les futurs traitements IA du Bloc 2.

L’agrégation finale constitue donc la dernière étape de préparation des données avant la mise en base et la mise à disposition.