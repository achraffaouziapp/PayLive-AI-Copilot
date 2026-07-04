# Nettoyage et normalisation des données — Bloc 1

## 1. Objectif

Cette étape a pour objectif de nettoyer, normaliser et fiabiliser les données collectées dans le cadre du projet **PayLive AI Copilot**.

Les données ont été collectées depuis plusieurs sources :

- fichiers CSV simulés ;
- API REST ;
- scraping web ;
- base SQL simulée ;
- source Big Data simulée.

Après la phase d’extraction, les données contiennent volontairement plusieurs anomalies :

- valeurs manquantes ;
- doublons ;
- formats hétérogènes ;
- statuts non normalisés ;
- dates invalides ;
- montants incohérents ;
- références inexistantes ;
- événements invalides.

Le nettoyage permet de transformer ces données brutes et intermédiaires en jeux de données propres, cohérents et exploitables pour la suite du projet.

## 2. Script utilisé

Le script utilisé est :

`src/data_processing/clean_and_standardize_data.py`

Ce script produit les fichiers nettoyés dans :

`data/processed/`

Il génère également des rapports de nettoyage permettant de tracer les corrections réalisées.

## 3. Position dans le pipeline de données

Le pipeline du Bloc 1 suit la logique suivante :

```text
1. Génération / collecte des données brutes
2. Extraction multi-sources
3. Analyse qualité des données extraites
4. Nettoyage et normalisation
5. Agrégation du dataset final
6. Stockage en base de données
7. Mise à disposition via API
```

Cette étape correspond donc à la phase :

```text
Analyse qualité -> Nettoyage -> Données propres
```

## 4. Sources utilisées

Le script utilise principalement les fichiers bruts situés dans :

`data/raw/`

Les fichiers utilisés sont :

```text
sellers_raw.csv
customers_raw.csv
products_raw.csv
live_sessions_raw.csv
live_products_raw.csv
live_comments_raw.csv
carts_raw.csv
cart_items_raw.csv
orders_raw.csv
payments_raw.csv
stock_movements_raw.csv
live_events_raw.csv
```

Pour les produits, le script utilise également les extractions issues de l’API et du scraping :

```text
data/interim/api_extracts/products_api_extract.csv
data/interim/scraping_extracts/products_scraped_extract.csv
```

Cela permet de construire un référentiel produit enrichi à partir de plusieurs sources.

## 5. Sorties générées

Le script génère les fichiers nettoyés suivants :

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

Il génère aussi des rapports techniques :

```text
data/processed/cleaning_summary.csv
data/processed/cleaning_operations_report.csv
data/processed/processed_manifest.csv
logs/clean_and_standardize_data.log
```

## 6. Règles générales de nettoyage

Le script applique plusieurs règles communes à tous les jeux de données.

### 6.1. Détection des valeurs manquantes

Les valeurs suivantes sont considérées comme manquantes :

```text
""
" "
"nan"
"NaN"
"none"
"None"
"null"
"NULL"
"n/a"
"N/A"
"unknown"
"UNKNOWN"
```

Ces valeurs sont ensuite remplacées, corrigées ou utilisées pour supprimer certaines lignes selon le contexte métier.

### 6.2. Nettoyage des chaînes de caractères

Toutes les colonnes texte sont nettoyées avec :

- suppression des espaces inutiles ;
- conversion de certains champs en minuscules ;
- standardisation des identifiants ;
- remplacement des valeurs textuelles incohérentes.

### 6.3. Suppression des clés primaires manquantes

Les lignes sans identifiant principal sont supprimées.

Exemples :

```text
seller_id manquant
customer_id manquant
product_id manquant
order_id manquant
payment_id manquant
```

Une ligne sans clé primaire ne peut pas être reliée correctement aux autres tables.

### 6.4. Suppression des doublons

Les doublons sont supprimés sur la base des clés primaires.

Exemple :

```text
Deux lignes avec le même seller_id
Deux lignes avec le même customer_id
Deux lignes avec le même order_id
```

Le script conserve la première occurrence.

### 6.5. Ajout de métadonnées de nettoyage

Chaque fichier nettoyé contient deux colonnes techniques :

```text
cleaned_at
data_quality_status
```

La colonne `cleaned_at` indique la date et l’heure du nettoyage.

La colonne `data_quality_status` contient la valeur :

```text
cleaned
```

Cela permet de tracer que les données ont bien été traitées.

## 7. Normalisation des valeurs catégorielles

Le script homogénéise les valeurs catégorielles afin d’éviter les variantes d’écriture.

### 7.1. Plateformes

Les plateformes sont normalisées avec les valeurs suivantes :

```text
tiktok
instagram
facebook_live
youtube_live
other
```

Exemples de corrections :

```text
TikTok        -> tiktok
tik tok       -> tiktok
tiktok_live   -> tiktok
IG            -> instagram
instagram live -> instagram
facebook      -> facebook_live
youtube       -> youtube_live
```

### 7.2. Statuts vendeurs

Les statuts vendeurs sont normalisés avec les valeurs suivantes :

```text
active
inactive
suspended
```

Exemples :

```text
actif     -> active
inactif   -> inactive
suspendu  -> suspended
```

### 7.3. Statuts produits

Les statuts produits sont normalisés avec les valeurs suivantes :

```text
active
inactive
out_of_stock
```

Si un produit possède un stock inférieur ou égal à zéro, son statut devient automatiquement :

```text
out_of_stock
```

### 7.4. Statuts de live

Les statuts de live sont normalisés avec les valeurs suivantes :

```text
scheduled
live
ended
cancelled
```

Exemples :

```text
planned   -> scheduled
finished  -> ended
canceled  -> cancelled
```

### 7.5. Statuts de panier

Les statuts de panier sont normalisés avec les valeurs suivantes :

```text
open
paid
abandoned
cancelled
```

### 7.6. Statuts de commande

Les statuts de commande sont normalisés avec les valeurs suivantes :

```text
pending
confirmed
paid
cancelled
refunded
```

### 7.7. Statuts de paiement

Les statuts de paiement sont normalisés avec les valeurs suivantes :

```text
pending
succeeded
failed
cancelled
refunded
```

Exemples :

```text
success -> succeeded
ok      -> succeeded
paid    -> succeeded
error   -> failed
```

### 7.8. Intentions des commentaires

Les intentions des commentaires sont normalisées avec les valeurs suivantes :

```text
purchase_intent
product_question
payment_question
shipping_question
other
unknown
```

Exemples :

```text
buy         -> purchase_intent
order       -> purchase_intent
reservation -> purchase_intent
```

### 7.9. Types d’événements

Les événements live sont normalisés avec les valeurs suivantes :

```text
comment_sent
cart_opened
payment_clicked
payment_succeeded
api_error
product_viewed
```

Les événements non reconnus sont supprimés.

## 8. Nettoyage par entité

## 8.1. Vendeurs — `sellers_clean.csv`

Le nettoyage des vendeurs applique les règles suivantes :

- suppression des lignes sans `seller_id` ;
- suppression des doublons sur `seller_id` ;
- normalisation de la plateforme principale ;
- normalisation du statut vendeur ;
- validation du format email ;
- remplacement des emails invalides par une valeur vide ;
- standardisation de la date de création.

Fichier généré :

`data/processed/sellers_clean.csv`

## 8.2. Clients — `customers_clean.csv`

Le nettoyage des clients applique les règles suivantes :

- suppression des lignes sans `customer_id` ;
- suppression des doublons sur `customer_id` ;
- normalisation de la plateforme ;
- remplacement des usernames manquants par `anonymous_user` ;
- validation du format email ;
- remplacement des emails invalides par une valeur vide ;
- standardisation de la date de création.

Fichier généré :

`data/processed/customers_clean.csv`

Cette approche permet de limiter l’exposition de données personnelles et de conserver des données cohérentes pour l’analyse.

## 8.3. Produits — `products_clean.csv`

Le nettoyage des produits est plus complet car il regroupe plusieurs sources :

- produits simulés ;
- produits issus de l’API ;
- produits issus du scraping.

Le script construit un référentiel produit commun avec les colonnes suivantes :

```text
product_id
product_name
category
brand
description
unit_price
stock_quantity
product_status
source
created_at
```

Les règles appliquées sont :

- suppression des lignes sans `product_id` ;
- suppression des doublons sur `product_id` ;
- normalisation des noms de produits ;
- normalisation des catégories ;
- standardisation des prix ;
- conversion des stocks en entiers ;
- remplacement des prix invalides ou négatifs par `0` ;
- remplacement des stocks invalides ou négatifs par `0` ;
- mise à jour automatique du statut `out_of_stock` si le stock est nul ;
- ajout d’un préfixe aux produits API ;
- ajout d’un préfixe aux produits scrapés.

Exemples d’identifiants produits enrichis :

```text
API_1
SCRAPED_abc123
```

Fichier généré :

`data/processed/products_clean.csv`

## 8.4. Sessions live — `live_sessions_clean.csv`

Le nettoyage des sessions live applique les règles suivantes :

- suppression des lignes sans `live_id` ;
- suppression des doublons sur `live_id` ;
- normalisation de `seller_id` ;
- normalisation de la plateforme ;
- normalisation du statut du live ;
- standardisation des dates ;
- conversion de `peak_viewers` en entier ;
- normalisation de la devise.

Fichier généré :

`data/processed/live_sessions_clean.csv`

## 8.5. Produits associés aux lives — `live_products_clean.csv`

Le nettoyage des produits associés aux lives applique les règles suivantes :

- suppression des lignes sans `live_product_id` ;
- suppression des doublons sur `live_product_id` ;
- normalisation de `live_id` ;
- normalisation de `product_id` ;
- conversion de `display_order` en entier ;
- conversion de `special_live_price` en nombre ;
- conversion de `initial_stock` en entier ;
- conversion de `remaining_stock` en entier.

Fichier généré :

`data/processed/live_products_clean.csv`

## 8.6. Commentaires live — `live_comments_clean.csv`

Le nettoyage des commentaires applique les règles suivantes :

- suppression des lignes sans `comment_id` ;
- suppression des doublons sur `comment_id` ;
- normalisation de `live_id` ;
- normalisation de `customer_id` ;
- normalisation de la plateforme ;
- remplacement des usernames manquants par `anonymous_user` ;
- suppression des commentaires vides ;
- standardisation de la date du commentaire ;
- normalisation de la langue ;
- normalisation du label d’intention ;
- nettoyage du mot-clé produit extrait.

Fichier généré :

`data/processed/live_comments_clean.csv`

Cette table sera importante pour les étapes IA, car elle contient les textes qui permettront plus tard de travailler sur la détection d’intention d’achat.

## 8.7. Paniers — `carts_clean.csv`

Le nettoyage des paniers applique les règles suivantes :

- suppression des lignes sans `cart_id` ;
- suppression des doublons sur `cart_id` ;
- normalisation de `live_id` ;
- normalisation de `customer_id` ;
- normalisation du statut du panier ;
- standardisation des dates ;
- conversion du montant total en nombre ;
- normalisation de la devise.

Fichier généré :

`data/processed/carts_clean.csv`

## 8.8. Articles de panier — `cart_items_clean.csv`

Le nettoyage des articles de panier applique les règles suivantes :

- suppression des lignes sans `cart_item_id` ;
- suppression des doublons sur `cart_item_id` ;
- normalisation de `cart_id` ;
- normalisation de `product_id` ;
- conversion de `quantity` en entier ;
- conversion de `unit_price` en nombre ;
- conversion de `line_total` en nombre ;
- normalisation de la taille sélectionnée ;
- normalisation de la couleur sélectionnée ;
- recalcul de `line_total` si le montant est incohérent.

La règle de recalcul est :

```text
line_total = quantity * unit_price
```

Fichier généré :

`data/processed/cart_items_clean.csv`

## 8.9. Commandes — `orders_clean.csv`

Le nettoyage des commandes applique les règles suivantes :

- suppression des lignes sans `order_id` ;
- suppression des doublons sur `order_id` ;
- normalisation de `cart_id` ;
- normalisation de `customer_id` ;
- normalisation de `seller_id` ;
- normalisation du statut de commande ;
- conversion du montant de commande ;
- normalisation de la devise ;
- standardisation des dates.

Fichier généré :

`data/processed/orders_clean.csv`

## 8.10. Paiements — `payments_clean.csv`

Le nettoyage des paiements applique les règles suivantes :

- suppression des lignes sans `payment_id` ;
- suppression des doublons sur `payment_id` ;
- normalisation de `order_id` ;
- normalisation du fournisseur de paiement ;
- normalisation du statut de paiement ;
- conversion du montant payé ;
- normalisation de la devise ;
- normalisation de la méthode de paiement ;
- standardisation de la date de paiement ;
- nettoyage de la référence de transaction.

Fichier généré :

`data/processed/payments_clean.csv`

Aucune donnée bancaire réelle n’est stockée. Les références de transaction sont fictives.

## 8.11. Mouvements de stock — `stock_movements_clean.csv`

Le nettoyage des mouvements de stock applique les règles suivantes :

- suppression des lignes sans `stock_movement_id` ;
- suppression des doublons sur `stock_movement_id` ;
- normalisation de `product_id` ;
- normalisation de `live_id` ;
- normalisation du type de mouvement ;
- conversion de `quantity_change` en entier ;
- normalisation de la raison du mouvement ;
- standardisation de la date.

Fichier généré :

`data/processed/stock_movements_clean.csv`

## 8.12. Événements live — `live_events_clean.csv`

Le nettoyage des événements live applique les règles suivantes :

- suppression des lignes sans `event_id` ;
- suppression des doublons sur `event_id` ;
- normalisation de `live_id` ;
- normalisation de `customer_id` ;
- normalisation du type d’événement ;
- suppression des événements de type invalide ;
- standardisation du timestamp ;
- suppression des événements avec timestamp invalide ;
- nettoyage de `event_value` ;
- normalisation du système source.

Fichier généré :

`data/processed/live_events_clean.csv`

## 9. Contrôle de l’intégrité référentielle

Après le nettoyage de chaque table, le script applique des contrôles de cohérence entre les datasets.

Les références invalides sont supprimées.

Exemples :

```text
live_sessions.seller_id doit exister dans sellers.seller_id
live_products.live_id doit exister dans live_sessions.live_id
live_products.product_id doit exister dans products.product_id
live_comments.live_id doit exister dans live_sessions.live_id
live_comments.customer_id doit exister dans customers.customer_id
carts.live_id doit exister dans live_sessions.live_id
carts.customer_id doit exister dans customers.customer_id
cart_items.cart_id doit exister dans carts.cart_id
cart_items.product_id doit exister dans products.product_id
orders.cart_id doit exister dans carts.cart_id
orders.customer_id doit exister dans customers.customer_id
orders.seller_id doit exister dans sellers.seller_id
payments.order_id doit exister dans orders.order_id
stock_movements.product_id doit exister dans products.product_id
stock_movements.live_id doit exister dans live_sessions.live_id
live_events.live_id doit exister dans live_sessions.live_id
live_events.customer_id doit exister dans customers.customer_id
```

Cette étape garantit que les tables nettoyées peuvent ensuite être stockées dans une base relationnelle cohérente.

## 10. Recalcul des montants financiers

Le script recalcule certains montants afin de corriger les incohérences détectées pendant l’analyse qualité.

### 10.1. Recalcul des lignes de panier

Pour chaque ligne de panier :

```text
line_total = quantity * unit_price
```

Si `line_total` est incohérent, il est remplacé par la valeur recalculée.

### 10.2. Recalcul du total panier

Pour chaque panier :

```text
total_amount = somme des line_total du panier
```

Si le montant total du panier est incohérent, il est remplacé par la somme des lignes associées.

### 10.3. Recalcul du montant commande

Pour chaque commande :

```text
order_amount = total_amount du panier lié
```

Si le montant de commande est incohérent, il est remplacé par le montant du panier associé.

### 10.4. Recalcul du montant de paiement

Pour les paiements réussis, si le montant est manquant ou nul, le script utilise le montant de la commande liée.

Cette règle évite de conserver un paiement réussi avec un montant inexploitable.

## 11. Rapports générés

## 11.1. Rapport de synthèse

Fichier :

`data/processed/cleaning_summary.csv`

Il contient, pour chaque dataset :

- nombre de lignes en entrée ;
- nombre de lignes en sortie ;
- nombre de lignes supprimées ;
- nombre de lignes supprimées pour clé primaire manquante ;
- nombre de doublons supprimés ;
- nombre de références invalides supprimées ;
- nombre de lignes métier invalides supprimées ;
- nombre de valeurs standardisées ;
- nombre de valeurs financières recalculées.

## 11.2. Rapport détaillé des opérations

Fichier :

`data/processed/cleaning_operations_report.csv`

Il contient le détail des opérations réalisées :

- timestamp de l’opération ;
- nom du dataset ;
- type d’opération ;
- nombre de lignes concernées ;
- description de l’opération.

Exemples d’opérations :

```text
missing_primary_key_removed
duplicate_rows_removed
invalid_reference_removed
invalid_business_rows_removed
values_standardized
financial_values_recalculated
```

## 11.3. Manifeste des datasets traités

Fichier :

`data/processed/processed_manifest.csv`

Il liste tous les fichiers générés avec :

- date de traitement ;
- nom du dataset ;
- chemin du fichier de sortie ;
- nombre de lignes ;
- nombre de colonnes ;
- statut de création.

## 11.4. Fichier de logs

Fichier :

`logs/clean_and_standardize_data.log`

Il permet de tracer l’exécution technique du script.

## 12. Résultat attendu

Après exécution du script :

```bash
python src/data_processing/clean_and_standardize_data.py
```

Le terminal doit afficher un message proche de :

```text
Data cleaning and standardization completed successfully.
Processed folder: .../data/processed
Cleaning summary: .../data/processed/cleaning_summary.csv
Cleaning operations report: .../data/processed/cleaning_operations_report.csv
Processed manifest: .../data/processed/processed_manifest.csv
```

Cela confirme que :

- les datasets ont été chargés ;
- les valeurs ont été standardisées ;
- les doublons ont été supprimés ;
- les références invalides ont été filtrées ;
- les montants financiers ont été recalculés ;
- les fichiers propres ont été générés ;
- les rapports de nettoyage ont été produits.

## 13. Justification RGPD

Les données utilisées dans ce projet sont simulées.

Aucune donnée réelle de l’entreprise PayLive n’est utilisée.

Les données personnelles présentes dans les fichiers sont fictives :

- noms ;
- emails ;
- usernames ;
- numéros de téléphone ;
- commentaires clients.

Les emails invalides sont supprimés ou remplacés par des valeurs vides.

Les usernames manquants sont remplacés par :

```text
anonymous_user
```

Aucune donnée bancaire réelle n’est stockée dans les paiements.

Cette approche limite les risques liés aux données personnelles et respecte le principe de minimisation des données.

## 14. Limites

Le nettoyage est basé sur des règles métier définies pour le projet.

Certaines décisions sont simplifiées :

- les doublons sont résolus en conservant la première occurrence ;
- les emails invalides sont vidés plutôt que corrigés ;
- les prix invalides sont remplacés par `0` ;
- les références étrangères invalides sont supprimées ;
- les événements invalides sont supprimés ;
- les statuts inconnus sont remplacés par une valeur par défaut.

Dans un projet réel, certaines corrections pourraient nécessiter une validation métier ou un arbitrage avec la source de données officielle.

## 15. Importance pour la suite du projet

Cette étape prépare les données pour :

- la création du dataset final agrégé ;
- le stockage dans une base relationnelle ;
- l’exposition des données via une API ;
- les traitements IA du Bloc 2 ;
- la construction de tableaux de bord ou d’indicateurs métier.

Les fichiers nettoyés constituent donc la base fiable du projet PayLive AI Copilot.

## 16. Conclusion

La phase de nettoyage et de normalisation permet de transformer des données hétérogènes, bruitées et partiellement corrompues en jeux de données cohérents.

Elle apporte :

- une meilleure qualité des données ;
- une structure homogène ;
- des identifiants fiables ;
- des relations cohérentes entre tables ;
- des montants financiers recalculés ;
- une traçabilité complète des opérations.

Cette étape finalise la préparation des données avant l’agrégation du dataset final.