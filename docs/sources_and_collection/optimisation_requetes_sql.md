# Optimisation des requêtes SQL et des traitements Big Data

## 1. Objectif du document

Ce document complète la documentation de collecte du Bloc 1. Il décrit les choix réalisés pour limiter le volume de données manipulé, réduire les traitements inutiles et rendre les extractions plus lisibles et plus efficaces. Il concerne principalement les extractions depuis la base SQL simulée ainsi que les traitements réalisés sur la source Big Data au format Parquet avec Spark.

L’objectif n’est pas de mettre en place une optimisation complexe comparable à celle d’un système de production à très grande échelle. Le projet reste une preuve de concept locale. En revanche, les requêtes et les traitements ont été structurés de manière à appliquer des principes réutilisables dans un contexte professionnel : sélectionner uniquement les données utiles, filtrer le plus tôt possible, limiter les jointures inutiles, réduire les volumes avant agrégation et exploiter les mécanismes d’indexation ou de partitionnement lorsque cela est pertinent.

Les optimisations présentées ci-dessous permettent également de justifier les choix de sélection, de filtrage, de jointure et de préparation des données nécessaires à la collecte.

---

## 2. Pourquoi utiliser des jointures ciblées

Les données métier sont réparties entre plusieurs entités : vendeurs, lives, clients, commentaires, paniers, commandes, paiements et produits. Une requête ne doit pas systématiquement joindre toutes les tables disponibles. Les jointures sont ajoutées uniquement lorsqu’une information provenant d’une autre table est nécessaire au résultat attendu.

Par exemple, lorsqu’une extraction doit relier un live à son vendeur, la jointure entre les tables de lives et de vendeurs est nécessaire afin de récupérer les informations du vendeur associées au `seller_id`. À l’inverse, il n’est pas utile d’ajouter les tables de paiements ou de commentaires si la requête ne porte que sur les informations générales du live.

Cette approche permet :

- de réduire le nombre de lignes intermédiaires produites ;
- de limiter le nombre de colonnes manipulées ;
- de rendre les requêtes plus simples à lire et à maintenir ;
- de réduire les risques de doublons introduits par des relations de type un-à-plusieurs ;
- d’éviter des calculs inutiles lorsque certaines tables ne sont pas nécessaires.

### Exemple de logique de jointure

```sql
SELECT
    l.live_id,
    l.seller_id,
    l.platform,
    l.live_status,
    s.shop_name
FROM live_sessions AS l
JOIN sellers AS s
    ON s.seller_id = l.seller_id;
```

Dans cet exemple, la jointure est justifiée car le nom de la boutique n’est pas stocké directement dans la table des lives. La clé `seller_id` permet d’associer les deux entités sans introduire de table supplémentaire.

> **Principe retenu :** une jointure n’est ajoutée que lorsqu’elle contribue directement à l’objectif de la requête.

---

## 3. Filtrage des colonnes

Une requête de collecte ne doit pas utiliser `SELECT *` par défaut lorsque seules certaines colonnes sont nécessaires. La sélection explicite des champs permet de contrôler précisément le contenu de l’extraction et de réduire le volume transféré entre la source et le script Python.

Par exemple, pour produire un indicateur de performance par live, il peut être suffisant de récupérer :

```text
live_id
seller_id
platform
live_status
peak_viewers
```

Il n’est pas nécessaire de charger simultanément toutes les colonnes liées aux dates, titres, devises ou métadonnées si elles ne sont pas utilisées dans le traitement concerné.

Cette stratégie apporte plusieurs avantages :

- moins de données transférées ;
- moins de mémoire utilisée côté Python ou Spark ;
- schéma d’extraction plus lisible ;
- réduction du risque d’utiliser involontairement une donnée non nécessaire ;
- meilleure maîtrise de la minimisation des données.

### Exemple

```sql
SELECT
    live_id,
    seller_id,
    platform,
    live_status,
    peak_viewers
FROM live_sessions;
```

La liste des colonnes est volontairement explicite afin de documenter le besoin de collecte.

---

## 4. Sélection des données utiles uniquement

L’optimisation ne concerne pas seulement les colonnes. Les lignes extraites doivent également correspondre au périmètre du traitement. Les clauses `WHERE` sont donc utilisées lorsque l’objectif métier permet de réduire le jeu de données dès la source.

Quelques exemples de filtres pertinents :

- exclure les enregistrements sans identifiant métier ;
- sélectionner uniquement une période de temps utile ;
- ne récupérer que les lives d’une plateforme donnée ;
- sélectionner les commandes appartenant à certains statuts ;
- limiter l’analyse aux événements nécessaires à une agrégation.

### Exemple

```sql
SELECT
    order_id,
    seller_id,
    order_status,
    order_amount,
    created_at
FROM orders
WHERE order_status IN ('confirmed', 'paid');
```

Le filtrage est réalisé dans la requête plutôt qu’après chargement complet du jeu de données. Cela évite de transférer puis de supprimer côté Python des lignes qui ne seront jamais utilisées.

> **Principe retenu :** rapprocher le filtrage au maximum de la source afin de réduire le volume traité dans les étapes suivantes.

---

## 5. Index PostgreSQL associés

Après nettoyage et import, les données sont stockées dans PostgreSQL. Des index sont créés sur les colonnes susceptibles d’être utilisées fréquemment dans les jointures, les filtres et les recherches de l’API.

Les index sont particulièrement utiles sur :

- les clés étrangères comme `seller_id`, `customer_id`, `live_id`, `cart_id`, `order_id` et `product_id` ;
- les colonnes de statut utilisées dans des filtres ;
- les dates utilisées pour les recherches chronologiques ;
- les colonnes de plateforme lorsque des analyses sont effectuées par canal ;
- les identifiants utilisés par les routes de détail de l’API.

### Exemple de logique d’indexation

```sql
CREATE INDEX IF NOT EXISTS idx_live_sessions_seller_id
    ON core.live_sessions (seller_id);

CREATE INDEX IF NOT EXISTS idx_live_comments_live_id
    ON core.live_comments (live_id);

CREATE INDEX IF NOT EXISTS idx_orders_seller_id
    ON core.orders (seller_id);

CREATE INDEX IF NOT EXISTS idx_payments_order_id
    ON core.payments (order_id);
```

Ces index réduisent le coût des recherches et des jointures portant sur les relations les plus fréquentes.

Il faut toutefois éviter de créer des index sur toutes les colonnes. Un index occupe de l’espace disque et doit être mis à jour lors des insertions ou modifications. Les index sont donc réservés aux colonnes présentant un intérêt réel pour les requêtes du projet.

> **Principe retenu :** indexer les colonnes réellement utilisées pour les relations, filtres et consultations fréquentes, sans sur-indexer la base.

---

## 6. Limitation des volumes de données

Le projet utilise des données simulées, mais les scripts sont conçus en gardant à l’esprit qu’un système réel pourrait contenir un volume beaucoup plus important de commentaires ou d’événements.

Plusieurs techniques permettent de limiter les volumes manipulés :

1. appliquer des filtres SQL avant le chargement ;
2. sélectionner uniquement les colonnes nécessaires ;
3. limiter le nombre de lignes lors des tests ou des phases de validation ;
4. agréger les données lorsque le détail n’est plus nécessaire ;
5. éviter de recopier plusieurs fois un même jeu de données intermédiaire ;
6. exploiter les partitions Parquet pour ne lire que les segments utiles.

Pour les tests de développement, une limitation peut également être appliquée avec une clause `LIMIT` afin de vérifier rapidement une requête avant de l’exécuter sur l’ensemble du jeu de données.

```sql
SELECT
    event_id,
    live_id,
    event_type,
    event_timestamp
FROM live_events
ORDER BY event_timestamp DESC
LIMIT 100;
```

Cette limitation ne remplace pas l’extraction complète utilisée pour produire les livrables finaux. Elle sert principalement aux tests, au débogage et à la validation d’une requête.

---

## 7. Filtrage avant agrégation

Lorsqu’une agrégation est nécessaire, le filtrage doit être appliqué avant les opérations coûteuses comme `GROUP BY`, les jointures multiples ou les calculs de statistiques.

Le principe est le suivant :

```text
source complète
    ↓
filtre sur le périmètre utile
    ↓
sélection des colonnes utiles
    ↓
jointures nécessaires
    ↓
agrégation
    ↓
résultat final
```

Cette organisation évite d’agréger des lignes qui seront ensuite supprimées.

### Exemple

```sql
SELECT
    live_id,
    COUNT(*) AS total_comments
FROM live_comments
WHERE commented_at IS NOT NULL
GROUP BY live_id;
```

Le contrôle sur `commented_at` est appliqué avant l’agrégation. Dans un volume plus important, cette logique réduit le nombre de lignes traitées par l’opération de regroupement.

La même logique est utilisée pour les événements Big Data : les types d’événements non nécessaires à l’analyse sont filtrés avant le calcul des indicateurs.

---

## 8. Partitionnement des fichiers Parquet

Le format Parquet est utilisé pour représenter la source Big Data car il est adapté au stockage analytique. Il s’agit d’un format colonnaire qui permet de ne lire que les colonnes nécessaires au traitement, contrairement à un format texte qui nécessite généralement de parcourir l’ensemble de la ligne.

Le partitionnement permet d’aller plus loin en organisant physiquement les données selon une ou plusieurs dimensions pertinentes, par exemple :

```text
platform=tiktok/
platform=instagram/
```

ou :

```text
year=2026/month=01/
year=2026/month=02/
```

Une requête portant uniquement sur une plateforme ou une période peut alors éviter la lecture des partitions non concernées.

### Exemple conceptuel

```python
spark.read.parquet("data/raw/bigdata/") \
    .filter("platform = 'tiktok'")
```

Lorsque la colonne utilisée pour le filtre correspond à une clé de partition, Spark peut limiter la lecture aux fichiers concernés. Ce mécanisme est généralement appelé **partition pruning**.

> **Principe retenu :** choisir des clés de partition cohérentes avec les filtres les plus courants afin de réduire les données réellement lues.

Dans le POC local, les volumes restent volontairement limités. Le partitionnement est donc surtout utilisé pour démontrer une organisation compatible avec un traitement Big Data plus important.

---

## 9. Réduction des données avant traitement Spark

Avec Spark, une optimisation importante consiste à réduire le jeu de données le plus tôt possible. Les transformations doivent donc privilégier les filtres et projections avant les agrégations ou jointures plus coûteuses.

Le traitement suit cette logique :

```text
lecture Parquet
    ↓
projection des colonnes nécessaires
    ↓
filtrage des lignes
    ↓
transformation métier
    ↓
agrégation Spark
    ↓
export du résultat
```

### Exemple conceptuel

```python
from pyspark.sql import functions as F

filtered_events = (
    events_df
    .select("live_id", "event_type", "event_timestamp")
    .filter(F.col("event_type").isin("comment", "cart_open", "payment_click", "api_error"))
)

summary_df = (
    filtered_events
    .groupBy("live_id", "event_type")
    .count()
)
```

Dans cet exemple, les colonnes inutiles sont supprimées avec `select()` et les types d’événements non concernés sont exclus avant le `groupBy()`.

Cette réduction précoce limite :

- la mémoire nécessaire ;
- le volume de données échangé entre les étapes Spark ;
- la quantité de données à agréger ;
- le temps de traitement lorsque les volumes deviennent importants.

> **Principe retenu :** filtrer et projeter avant les traitements distribués les plus coûteux.

---

## 10. Synthèse des optimisations appliquées

| Axe d’optimisation | Application dans le projet | Objectif |
|---|---|---|
| Jointures ciblées | Jointure uniquement avec les tables nécessaires | Réduire les traitements intermédiaires |
| Projection de colonnes | Sélection explicite des champs | Limiter le volume transféré |
| Filtres SQL | `WHERE` avant chargement | Réduire le nombre de lignes |
| Index PostgreSQL | Index sur clés et colonnes fréquemment interrogées | Accélérer jointures et recherches |
| Limitation des volumes | `LIMIT` en phase de test, agrégations et filtres | Accélérer validation et débogage |
| Filtre avant agrégation | Filtrage avant `GROUP BY` | Réduire le coût des agrégations |
| Parquet | Format colonnaire | Lire uniquement les colonnes utiles |
| Partitionnement Parquet | Partition par dimension pertinente | Éviter la lecture de partitions inutiles |
| Réduction avant Spark | `select()` + `filter()` avant `groupBy()` | Réduire les traitements distribués |

---

## 11. Traçabilité et reproductibilité

Les requêtes d’extraction, les scripts de collecte et les scripts de traitement sont conservés dans le dépôt Git du projet. Cette organisation permet de relancer les extractions et de comprendre les choix appliqués sans dépendre d’une manipulation manuelle effectuée directement dans un outil de base de données.

Les éléments techniques concernés sont principalement :

```text
src/data_collection/collect_from_database.py
src/data_collection/collect_from_bigdata.py
sql/
data/interim/extracts/database/
data/interim/extracts/bigdata/
data/interim/reports/database_collection/
data/interim/reports/bigdata_collection/
```

La documentation complète les scripts en expliquant non seulement **ce qui est exécuté**, mais également **pourquoi les requêtes et transformations ont été structurées de cette manière**.

---

## 12. Limites et améliorations possibles

Les volumes utilisés dans le projet restent limités et simulés. Les optimisations décrites sont donc principalement des choix d’architecture et de préparation à une montée en charge, plutôt que le résultat d’un benchmark de plusieurs milliards de lignes.

Dans une version de production, plusieurs améliorations pourraient être ajoutées :

- mesure des temps d’exécution avec et sans index ;
- analyse des plans PostgreSQL avec `EXPLAIN ANALYZE` ;
- suivi du coût des requêtes ;
- index composites sur les filtres les plus fréquents ;
- partitionnement natif PostgreSQL sur les tables volumineuses ;
- cache des requêtes analytiques fréquentes ;
- mesure des volumes lus par Spark ;
- optimisation du nombre de partitions Spark ;
- suivi des opérations de shuffle ;
- tests de performance automatisés.

Ces évolutions seraient pertinentes si le volume de données ou le nombre d’utilisateurs augmentait fortement.

---

## 13. Conclusion

L’optimisation des requêtes et des traitements repose sur un principe simple : **réduire le plus tôt possible les données à manipuler tout en conservant uniquement les informations nécessaires au besoin métier**.

La collecte SQL privilégie donc les jointures ciblées, les colonnes explicitement sélectionnées et les filtres en amont. PostgreSQL utilise des index sur les relations et recherches fréquentes. Pour la source Big Data, le format Parquet, le partitionnement et la réduction des données avant agrégation Spark permettent de limiter les traitements inutiles.

Cette démarche rend les scripts plus lisibles, plus reproductibles et mieux préparés à une augmentation future du volume de données.
