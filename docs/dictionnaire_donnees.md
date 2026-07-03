# Dictionnaire des données — Bloc 1

## Projet : PayLive AI Copilot

## 1. Objectif du dictionnaire des données

Ce document définit les données utilisées dans le Bloc 1 du projet **PayLive AI Copilot**.

Il sert de référence pour :

* la simulation des données ;
* la collecte des données depuis plusieurs sources ;
* le nettoyage et la normalisation ;
* l’agrégation des données ;
* la modélisation Merise ;
* la création de la base PostgreSQL ;
* le développement de l’API REST ;
* la documentation RGPD.

Aucune donnée réelle de l’entreprise n’est utilisée. Les données sont simulées ou collectées depuis des sources publiques de test.

## 2. Vision générale du modèle de données

Le système doit représenter l’activité d’un vendeur qui réalise des ventes pendant un live TikTok ou Instagram.

Les principales entités sont :

* vendeur ;
* client ou spectateur ;
* session live ;
* produit ;
* commentaire ;
* panier ;
* article de panier ;
* commande ;
* paiement ;
* mouvement de stock ;
* événement technique ou comportemental.

## 3. Relations principales entre les entités

Les relations principales sont les suivantes :

* un vendeur peut organiser plusieurs sessions live ;
* une session live appartient à un vendeur ;
* une session live peut présenter plusieurs produits ;
* un produit peut être présenté dans plusieurs sessions live ;
* une session live peut recevoir plusieurs commentaires ;
* un client peut publier plusieurs commentaires ;
* un commentaire peut contenir une intention d’achat ;
* un client peut avoir plusieurs paniers ;
* un panier appartient à une session live ;
* un panier peut contenir plusieurs articles ;
* un panier peut générer une commande ;
* une commande peut avoir un ou plusieurs paiements ;
* un produit peut avoir plusieurs mouvements de stock ;
* une session live peut générer plusieurs événements techniques ou comportementaux.

## 4. Convention de nommage

Les identifiants techniques suivent une convention simple :

* `seller_id` pour les vendeurs ;
* `customer_id` pour les clients ;
* `live_id` pour les sessions live ;
* `product_id` pour les produits ;
* `comment_id` pour les commentaires ;
* `cart_id` pour les paniers ;
* `order_id` pour les commandes ;
* `payment_id` pour les paiements ;
* `event_id` pour les événements.

Les dates sont normalisées au format ISO :

```text
YYYY-MM-DD HH:MM:SS
```

Les montants sont stockés en euros avec deux décimales.

## 5. Table : sellers

### Description

La table `sellers` contient les informations des vendeurs utilisant la plateforme.

### Source prévue

* fichier simulé `sellers_raw.csv` ;
* base SQL source simulée `legacy_sellers`.

### Colonnes

| Colonne          |   Type cible | Obligatoire | Description                                        | Donnée personnelle |
| ---------------- | -----------: | ----------: | -------------------------------------------------- | -----------------: |
| seller_id        |  VARCHAR(20) |         Oui | Identifiant unique du vendeur                      |                Non |
| shop_name        | VARCHAR(100) |         Oui | Nom commercial de la boutique                      |                Non |
| owner_first_name |  VARCHAR(80) |         Non | Prénom fictif du responsable                       |                Oui |
| owner_last_name  |  VARCHAR(80) |         Non | Nom fictif du responsable                          |                Oui |
| email            | VARCHAR(150) |         Oui | Email professionnel fictif                         |                Oui |
| phone_number     |  VARCHAR(30) |         Non | Numéro fictif                                      |                Oui |
| country          |  VARCHAR(80) |         Oui | Pays du vendeur                                    |                Non |
| main_platform    |  VARCHAR(30) |         Oui | Plateforme principale : TikTok, Instagram ou autre |                Non |
| created_at       |    TIMESTAMP |         Oui | Date de création du vendeur                        |                Non |
| seller_status    |  VARCHAR(30) |         Oui | Statut : active, inactive, suspended               |                Non |

### Défauts à simuler

* emails invalides ;
* doublons sur `seller_id` ;
* doublons sur `email` ;
* pays manquant ;
* plateforme écrite sous plusieurs formes : `TikTok`, `tiktok`, `tik tok` ;
* statut invalide : `actif`, `ok`, `deleted`.

## 6. Table : customers

### Description

La table `customers` contient les informations des spectateurs ou acheteurs simulés.

### Source prévue

* commentaires de live ;
* paiements simulés ;
* paniers simulés.

### Colonnes

| Colonne     |   Type cible | Obligatoire | Description                           | Donnée personnelle |
| ----------- | -----------: | ----------: | ------------------------------------- | -----------------: |
| customer_id |  VARCHAR(20) |         Oui | Identifiant pseudonymisé du client    |                Non |
| username    | VARCHAR(100) |         Oui | Nom d’utilisateur de la plateforme    |                Oui |
| platform    |  VARCHAR(30) |         Oui | TikTok ou Instagram                   |                Non |
| email       | VARCHAR(150) |         Non | Email fictif du client                |                Oui |
| country     |  VARCHAR(80) |         Non | Pays simulé                           |                Non |
| created_at  |    TIMESTAMP |         Oui | Date de première apparition du client |                Non |

### Défauts à simuler

* username manquant ;
* email invalide ;
* doublons de clients avec usernames proches ;
* plateformes non normalisées ;
* pays manquant.

### Précaution RGPD

Les clients seront pseudonymisés. Les noms d’utilisateurs et emails seront fictifs.

## 7. Table : live_sessions

### Description

La table `live_sessions` contient les informations des sessions de vente en direct.

### Source prévue

* fichier simulé `live_sessions_raw.csv` ;
* base SQL source simulée `legacy_live_sessions`.

### Colonnes

| Colonne            |   Type cible | Obligatoire | Description                       | Donnée personnelle |
| ------------------ | -----------: | ----------: | --------------------------------- | -----------------: |
| live_id            |  VARCHAR(20) |         Oui | Identifiant unique du live        |                Non |
| seller_id          |  VARCHAR(20) |         Oui | Vendeur associé au live           |                Non |
| platform           |  VARCHAR(30) |         Oui | TikTok, Instagram ou autre        |                Non |
| live_title         | VARCHAR(150) |         Oui | Titre du live                     |                Non |
| scheduled_start_at |    TIMESTAMP |         Non | Date prévue du live               |                Non |
| actual_start_at    |    TIMESTAMP |         Oui | Date réelle de début              |                Non |
| ended_at           |    TIMESTAMP |         Non | Date de fin                       |                Non |
| live_status        |  VARCHAR(30) |         Oui | scheduled, live, ended, cancelled |                Non |
| peak_viewers       |      INTEGER |         Non | Nombre maximal de spectateurs     |                Non |
| currency           |  VARCHAR(10) |         Oui | Devise utilisée                   |                Non |
| created_at         |    TIMESTAMP |         Oui | Date de création de la session    |                Non |

### Défauts à simuler

* `seller_id` inexistant ;
* date de fin avant date de début ;
* date invalide ;
* statut non reconnu ;
* devise manquante ;
* plateforme non normalisée ;
* doublons de `live_id`.

## 8. Table : products

### Description

La table `products` contient le catalogue des produits vendus ou présentés pendant les lives.

### Source prévue

* API externe de produits ;
* scraping d’un site de test ;
* fichier simulé complémentaire.

### Colonnes

| Colonne        |    Type cible | Obligatoire | Description                         | Donnée personnelle |
| -------------- | ------------: | ----------: | ----------------------------------- | -----------------: |
| product_id     |   VARCHAR(20) |         Oui | Identifiant unique du produit       |                Non |
| product_name   |  VARCHAR(150) |         Oui | Nom du produit                      |                Non |
| category       |   VARCHAR(80) |         Oui | Catégorie du produit                |                Non |
| brand          |   VARCHAR(80) |         Non | Marque du produit                   |                Non |
| description    |          TEXT |         Non | Description du produit              |                Non |
| unit_price     | DECIMAL(10,2) |         Oui | Prix unitaire                       |                Non |
| stock_quantity |       INTEGER |         Oui | Stock disponible                    |                Non |
| product_status |   VARCHAR(30) |         Oui | active, inactive, out_of_stock      |                Non |
| source         |   VARCHAR(50) |         Oui | Origine : API, scraping, simulation |                Non |
| created_at     |     TIMESTAMP |         Oui | Date d’intégration du produit       |                Non |

### Défauts à simuler

* produit dupliqué ;
* prix manquant ;
* prix négatif ;
* stock négatif ;
* catégorie non normalisée ;
* nom produit avec casse différente ;
* produit sans description ;
* marque manquante.

## 9. Table : live_products

### Description

La table `live_products` relie les produits aux sessions live.

Elle permet de savoir quels produits ont été présentés pendant un live.

### Source prévue

* fichier simulé `live_products_raw.csv`.

### Colonnes

| Colonne            |    Type cible | Obligatoire | Description                                      | Donnée personnelle |
| ------------------ | ------------: | ----------: | ------------------------------------------------ | -----------------: |
| live_product_id    |   VARCHAR(20) |         Oui | Identifiant unique de l’association live-produit |                Non |
| live_id            |   VARCHAR(20) |         Oui | Identifiant du live                              |                Non |
| product_id         |   VARCHAR(20) |         Oui | Identifiant du produit                           |                Non |
| display_order      |       INTEGER |         Non | Ordre de présentation pendant le live            |                Non |
| special_live_price | DECIMAL(10,2) |         Non | Prix spécial pendant le live                     |                Non |
| initial_stock      |       INTEGER |         Non | Stock disponible au début du live                |                Non |
| remaining_stock    |       INTEGER |         Non | Stock restant à la fin du live                   |                Non |

### Défauts à simuler

* `product_id` inexistant ;
* `live_id` inexistant ;
* prix spécial supérieur au prix normal ;
* stock restant supérieur au stock initial ;
* doublons sur le couple `live_id` + `product_id`.

## 10. Table : live_comments

### Description

La table `live_comments` contient les commentaires publiés pendant les lives.

Cette table sera très importante pour les blocs suivants, car elle servira de base à l’analyse IA des intentions d’achat.

### Source prévue

* fichier simulé `live_comments_raw.csv` ;
* logs big data simulés.

### Colonnes

| Colonne                   |   Type cible | Obligatoire | Description                                                | Donnée personnelle |
| ------------------------- | -----------: | ----------: | ---------------------------------------------------------- | -----------------: |
| comment_id                |  VARCHAR(30) |         Oui | Identifiant unique du commentaire                          |                Non |
| live_id                   |  VARCHAR(20) |         Oui | Live concerné                                              |                Non |
| customer_id               |  VARCHAR(20) |         Non | Client ou spectateur associé                               |                Non |
| platform                  |  VARCHAR(30) |         Oui | TikTok ou Instagram                                        |                Non |
| username                  | VARCHAR(100) |         Non | Nom d’utilisateur fictif                                   |                Oui |
| comment_text              |         TEXT |         Oui | Texte du commentaire                                       |                Oui |
| commented_at              |    TIMESTAMP |         Oui | Date du commentaire                                        |                Non |
| comment_language          |  VARCHAR(10) |         Non | Langue détectée ou simulée                                 |                Non |
| manual_intent_label       |  VARCHAR(50) |         Non | Label simulé : purchase_intent, question, complaint, other |                Non |
| extracted_product_keyword | VARCHAR(100) |         Non | Mot-clé produit extrait manuellement ou simulé             |                Non |
| data_quality_status       |  VARCHAR(30) |         Oui | valid, incomplete, duplicate, corrupted                    |                Non |

### Défauts à simuler

* commentaires dupliqués ;
* texte vide ;
* date invalide ;
* `live_id` manquant ;
* username manquant ;
* plateformes mal écrites ;
* commentaires avec fautes ;
* intentions d’achat ambiguës ;
* plusieurs formats de date.

### Exemples de commentaires simulés

```text
Je prends la robe rouge en M
Prix ?
Réserve-moi le bleu taille L
Je veux 2 pièces
Dispo en noir ?
C’est trop cher
Je paye comment ?
```

## 11. Table : carts

### Description

La table `carts` représente les paniers créés pendant ou après un live.

### Source prévue

* fichier simulé `carts_raw.csv` ;
* génération à partir des commentaires d’intention d’achat.

### Colonnes

| Colonne      |    Type cible | Obligatoire | Description                                          | Donnée personnelle |
| ------------ | ------------: | ----------: | ---------------------------------------------------- | -----------------: |
| cart_id      |   VARCHAR(20) |         Oui | Identifiant unique du panier                         |                Non |
| live_id      |   VARCHAR(20) |         Oui | Live d’origine                                       |                Non |
| customer_id  |   VARCHAR(20) |         Oui | Client associé                                       |                Non |
| cart_status  |   VARCHAR(30) |         Oui | created, pending_payment, paid, abandoned, cancelled |                Non |
| created_at   |     TIMESTAMP |         Oui | Date de création du panier                           |                Non |
| updated_at   |     TIMESTAMP |         Non | Date de dernière modification                        |                Non |
| total_amount | DECIMAL(10,2) |         Oui | Montant total du panier                              |                Non |
| currency     |   VARCHAR(10) |         Oui | Devise                                               |                Non |

### Défauts à simuler

* panier sans client ;
* panier sans live ;
* montant total incohérent ;
* statut invalide ;
* devise manquante ;
* date de mise à jour avant la date de création.

## 12. Table : cart_items

### Description

La table `cart_items` contient les lignes de produits dans les paniers.

### Source prévue

* fichier simulé `cart_items_raw.csv`.

### Colonnes

| Colonne        |    Type cible | Obligatoire | Description                           | Donnée personnelle |
| -------------- | ------------: | ----------: | ------------------------------------- | -----------------: |
| cart_item_id   |   VARCHAR(20) |         Oui | Identifiant unique de la ligne panier |                Non |
| cart_id        |   VARCHAR(20) |         Oui | Panier associé                        |                Non |
| product_id     |   VARCHAR(20) |         Oui | Produit ajouté                        |                Non |
| quantity       |       INTEGER |         Oui | Quantité commandée                    |                Non |
| unit_price     | DECIMAL(10,2) |         Oui | Prix unitaire au moment de l’achat    |                Non |
| line_total     | DECIMAL(10,2) |         Oui | Total de la ligne                     |                Non |
| selected_size  |   VARCHAR(20) |         Non | Taille demandée                       |                Non |
| selected_color |   VARCHAR(50) |         Non | Couleur demandée                      |                Non |

### Défauts à simuler

* quantité égale à zéro ;
* quantité négative ;
* prix unitaire manquant ;
* total de ligne incorrect ;
* taille non normalisée : `m`, `Medium`, `meduim` ;
* couleur non normalisée : `red`, `roug`, `rge`.

## 13. Table : orders

### Description

La table `orders` représente les commandes générées à partir des paniers.

### Source prévue

* fichier simulé `orders_raw.csv` ;
* base SQL source simulée `legacy_orders`.

### Colonnes

| Colonne      |    Type cible | Obligatoire | Description                                   | Donnée personnelle |
| ------------ | ------------: | ----------: | --------------------------------------------- | -----------------: |
| order_id     |   VARCHAR(20) |         Oui | Identifiant unique de la commande             |                Non |
| cart_id      |   VARCHAR(20) |         Oui | Panier d’origine                              |                Non |
| customer_id  |   VARCHAR(20) |         Oui | Client associé                                |                Non |
| seller_id    |   VARCHAR(20) |         Oui | Vendeur associé                               |                Non |
| order_status |   VARCHAR(30) |         Oui | pending, confirmed, paid, cancelled, refunded |                Non |
| order_amount | DECIMAL(10,2) |         Oui | Montant de la commande                        |                Non |
| currency     |   VARCHAR(10) |         Oui | Devise                                        |                Non |
| created_at   |     TIMESTAMP |         Oui | Date de création de la commande               |                Non |
| confirmed_at |     TIMESTAMP |         Non | Date de confirmation                          |                Non |

### Défauts à simuler

* commande sans panier ;
* commande sans client ;
* montant incohérent avec le panier ;
* statut contradictoire avec le paiement ;
* date de confirmation avant date de création ;
* doublons sur `order_id`.

## 14. Table : payments

### Description

La table `payments` contient les informations de paiement simulées.

Aucune donnée bancaire réelle n’est stockée.

### Source prévue

* fichier simulé `payments_raw.csv` ;
* API de paiement simulée ;
* base SQL source simulée `legacy_payments`.

### Colonnes

| Colonne               |    Type cible | Obligatoire | Description                                       | Donnée personnelle |
| --------------------- | ------------: | ----------: | ------------------------------------------------- | -----------------: |
| payment_id            |   VARCHAR(20) |         Oui | Identifiant unique du paiement                    |                Non |
| order_id              |   VARCHAR(20) |         Oui | Commande associée                                 |                Non |
| payment_provider      |   VARCHAR(50) |         Oui | Prestataire simulé : stripe, paypal, paylive_mock |                Non |
| payment_status        |   VARCHAR(30) |         Oui | pending, succeeded, failed, refunded              |                Non |
| payment_amount        | DECIMAL(10,2) |         Oui | Montant payé                                      |                Non |
| currency              |   VARCHAR(10) |         Oui | Devise                                            |                Non |
| payment_method        |   VARCHAR(30) |         Non | card, wallet, bank_transfer                       |                Non |
| paid_at               |     TIMESTAMP |         Non | Date du paiement                                  |                Non |
| transaction_reference |  VARCHAR(100) |         Non | Référence fictive de transaction                  |                Non |

### Défauts à simuler

* montant de paiement différent de la commande ;
* statut invalide ;
* paiement réussi sans date de paiement ;
* devise différente de la commande ;
* référence transaction dupliquée ;
* paiement lié à une commande inexistante.

## 15. Table : stock_movements

### Description

La table `stock_movements` permet de suivre les variations de stock.

### Source prévue

* fichier simulé `stock_movements_raw.csv`.

### Colonnes

| Colonne           |   Type cible | Obligatoire | Description                       | Donnée personnelle |
| ----------------- | -----------: | ----------: | --------------------------------- | -----------------: |
| stock_movement_id |  VARCHAR(20) |         Oui | Identifiant du mouvement de stock |                Non |
| product_id        |  VARCHAR(20) |         Oui | Produit concerné                  |                Non |
| live_id           |  VARCHAR(20) |         Non | Live concerné si applicable       |                Non |
| movement_type     |  VARCHAR(30) |         Oui | sale, return, adjustment, restock |                Non |
| quantity_change   |      INTEGER |         Oui | Variation de quantité             |                Non |
| movement_reason   | VARCHAR(150) |         Non | Raison du mouvement               |                Non |
| created_at        |    TIMESTAMP |         Oui | Date du mouvement                 |                Non |

### Défauts à simuler

* produit inexistant ;
* quantité nulle ;
* mouvement incohérent ;
* date invalide ;
* type de mouvement non reconnu.

## 16. Table : live_events

### Description

La table `live_events` contient les événements techniques ou comportementaux générés pendant un live.

Elle représente la source de type big data du projet.

### Source prévue

* fichiers Parquet simulés ;
* traitement PySpark.

### Colonnes

| Colonne         |   Type cible | Obligatoire | Description                                                              | Donnée personnelle |
| --------------- | -----------: | ----------: | ------------------------------------------------------------------------ | -----------------: |
| event_id        |  VARCHAR(30) |         Oui | Identifiant unique de l’événement                                        |                Non |
| live_id         |  VARCHAR(20) |         Oui | Live concerné                                                            |                Non |
| customer_id     |  VARCHAR(20) |         Non | Client concerné si applicable                                            |                Non |
| event_type      |  VARCHAR(50) |         Oui | comment_sent, cart_opened, payment_clicked, payment_succeeded, api_error |                Non |
| event_timestamp |    TIMESTAMP |         Oui | Date de l’événement                                                      |                Non |
| event_value     | VARCHAR(150) |         Non | Valeur complémentaire                                                    |                Non |
| source_system   |  VARCHAR(50) |         Oui | Origine de l’événement                                                   |                Non |

### Défauts à simuler

* événements dupliqués ;
* timestamp invalide ;
* live inexistant ;
* type d’événement inconnu ;
* client manquant ;
* source système manquante.

## 17. Dataset final agrégé

### Nom du fichier

```text
dataset_final_live_sales.csv
```

### Objectif

Le dataset final agrégé servira à analyser les performances des lives et à préparer les futurs traitements IA.

### Colonnes prévues

| Colonne                  | Description                                   |
| ------------------------ | --------------------------------------------- |
| live_id                  | Identifiant du live                           |
| seller_id                | Identifiant du vendeur                        |
| platform                 | Plateforme du live                            |
| live_date                | Date du live                                  |
| total_comments           | Nombre total de commentaires                  |
| purchase_intent_comments | Nombre de commentaires avec intention d’achat |
| total_carts              | Nombre de paniers créés                       |
| paid_carts               | Nombre de paniers payés                       |
| abandoned_carts          | Nombre de paniers abandonnés                  |
| total_orders             | Nombre total de commandes                     |
| total_revenue            | Chiffre d’affaires total                      |
| average_order_amount     | Panier moyen                                  |
| payment_success_rate     | Taux de paiement réussi                       |
| top_product_category     | Catégorie la plus vendue                      |
| peak_viewers             | Pic de spectateurs                            |
| conversion_rate          | Taux de conversion approximatif               |

### Défauts à traiter avant génération

Le dataset final ne devra contenir que des données nettoyées et cohérentes.

Les données invalides devront être :

* corrigées si possible ;
* supprimées si elles sont inutilisables ;
* isolées dans un fichier de rejet si nécessaire.

## 18. Règles de qualité des données

Les règles générales de qualité sont les suivantes :

* les identifiants principaux ne doivent pas être vides ;
* les dates doivent être convertibles au format standard ;
* les montants doivent être positifs ou nuls selon le contexte ;
* les statuts doivent appartenir à une liste autorisée ;
* les plateformes doivent être normalisées ;
* les doublons doivent être détectés ;
* les relations entre tables doivent être cohérentes ;
* les données personnelles doivent être fictives ou pseudonymisées.

## 19. Listes de valeurs autorisées

### Plateformes

```text
tiktok
instagram
facebook_live
youtube_live
other
```

### Statuts de live

```text
scheduled
live
ended
cancelled
```

### Statuts de panier

```text
created
pending_payment
paid
abandoned
cancelled
```

### Statuts de commande

```text
pending
confirmed
paid
cancelled
refunded
```

### Statuts de paiement

```text
pending
succeeded
failed
refunded
```

### Intentions de commentaire

```text
purchase_intent
price_question
stock_question
payment_question
complaint
other
```

### Tailles normalisées

```text
XS
S
M
L
XL
XXL
unique
unknown
```

### Couleurs normalisées

```text
black
white
red
blue
green
yellow
pink
beige
brown
grey
unknown
```

## 20. Données personnelles et RGPD

Même si les données sont fictives, certaines colonnes sont traitées comme des données personnelles afin de respecter une logique RGPD.

Les colonnes concernées sont :

* `owner_first_name` ;
* `owner_last_name` ;
* `email` ;
* `phone_number` ;
* `username` ;
* `comment_text`.

Les mesures appliquées sont :

* utilisation de données fictives ;
* pseudonymisation des clients avec `customer_id` ;
* absence de données bancaires réelles ;
* absence de numéro de carte bancaire ;
* limitation des données personnelles collectées ;
* documentation des traitements ;
* possibilité de suppression d’un client simulé ;
* séparation entre données techniques et données personnelles.

## 21. Fichiers bruts à générer

Les fichiers bruts prévus sont :

```text
data/raw/sellers_raw.csv
data/raw/customers_raw.csv
data/raw/live_sessions_raw.csv
data/raw/products_api_raw.json
data/raw/products_scraped_raw.csv
data/raw/live_products_raw.csv
data/raw/live_comments_raw.csv
data/raw/carts_raw.csv
data/raw/cart_items_raw.csv
data/raw/orders_raw.csv
data/raw/payments_raw.csv
data/raw/stock_movements_raw.csv
data/raw/live_events_raw.parquet
```

## 22. Fichiers propres attendus

Les fichiers propres attendus sont :

```text
data/processed/dim_sellers.csv
data/processed/dim_customers.csv
data/processed/dim_products.csv
data/processed/fact_live_sessions.csv
data/processed/fact_live_comments.csv
data/processed/fact_carts.csv
data/processed/fact_orders.csv
data/processed/fact_payments.csv
data/processed/fact_stock_movements.csv
data/processed/fact_live_events.csv
data/processed/dataset_final_live_sales.csv
```

## 23. Conclusion

Ce dictionnaire des données définit la base du Bloc 1 du projet PayLive AI Copilot.

Il permet de préparer la simulation, la collecte, le nettoyage, le stockage et la mise à disposition des données.

Il servira également de support pour la modélisation Merise, la création de la base PostgreSQL, le développement de l’API REST et la rédaction de la documentation RGPD.
