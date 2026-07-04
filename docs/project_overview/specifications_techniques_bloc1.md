# Spécifications techniques — Bloc 1

## 1. Objectif technique

Le Bloc 1 a pour objectif de construire une chaîne technique complète permettant de collecter, nettoyer, stocker et exposer les données nécessaires au projet PayLive AI Copilot.

Le système doit permettre de récupérer des données depuis plusieurs sources, de les transformer en un jeu de données cohérent, de les stocker dans une base relationnelle et de les rendre disponibles via une API REST.

## 2. Périmètre technique

Le périmètre du Bloc 1 couvre les éléments suivants :

* collecte de données depuis une API externe ;
* collecte de données depuis des fichiers CSV ou JSON ;
* collecte de données par scraping sur un site de test autorisé ;
* extraction de données depuis une base SQL source simulée ;
* traitement de fichiers volumineux simulés avec une approche big data ;
* nettoyage des données ;
* normalisation des formats ;
* agrégation des données ;
* création d’une base PostgreSQL ;
* import des données nettoyées ;
* développement d’une API REST ;
* sécurisation de l’accès à l’API ;
* documentation technique.

## 3. Technologies retenues

Les technologies proposées pour le Bloc 1 sont :

* Python pour les scripts de collecte, nettoyage et agrégation ;
* Pandas pour le traitement des données tabulaires ;
* Requests pour les appels API ;
* BeautifulSoup ou Scrapy pour le scraping de site de test ;
* PostgreSQL pour la base de données relationnelle ;
* SQL pour les requêtes d’extraction, de contrôle et d’analyse ;
* PySpark pour simuler le traitement de fichiers volumineux ;
* FastAPI pour l’API REST ;
* Swagger / OpenAPI pour la documentation de l’API ;
* Docker pour faciliter l’installation de la base et de l’API ;
* Git pour le versionnement du code et des documents.

## 4. Sources de données prévues

Les données seront collectées depuis plusieurs sources :

* API publique de test pour récupérer un catalogue produit ;
* fichiers CSV/JSON simulant les commentaires, paiements, vendeurs et sessions live ;
* scraping d’un site e-commerce de test autorisé ;
* base SQL source simulant un ancien système ;
* fichiers Parquet simulant des logs d’événements volumineux.

## 5. Données attendues

Les principales entités manipulées sont :

* vendeur ;
* client ou utilisateur live ;
* session live ;
* commentaire ;
* produit ;
* panier ;
* commande ;
* paiement ;
* événement technique ;
* statistique de live.

## 6. Règles générales de traitement

Les scripts devront respecter les règles suivantes :

* conserver une copie brute des données collectées ;
* ne jamais modifier directement les fichiers du dossier `data/raw` ;
* produire des fichiers intermédiaires dans `data/interim` ;
* produire des fichiers propres dans `data/processed` ;
* documenter les règles de nettoyage ;
* détecter les doublons ;
* identifier les valeurs manquantes ;
* normaliser les formats de dates ;
* normaliser les plateformes ;
* normaliser les tailles ;
* normaliser les couleurs ;
* contrôler la cohérence des montants ;
* supprimer ou isoler les lignes corrompues ;
* produire un dataset final exploitable.

## 7. Règles de sécurité

L’API REST devra intégrer des règles de sécurité minimales :

* authentification par token ;
* restriction d’accès aux endpoints sensibles ;
* validation des paramètres envoyés par les clients ;
* gestion des erreurs ;
* absence d’exposition d’informations sensibles dans les réponses ;
* séparation des variables d’environnement dans un fichier `.env`.

## 8. Contraintes RGPD

Même si les données sont simulées, le projet doit appliquer une logique RGPD.

Les règles suivantes seront appliquées :

* minimisation des données personnelles ;
* utilisation de données fictives ;
* pseudonymisation des identifiants clients ;
* absence de données bancaires réelles ;
* conservation limitée des données simulées ;
* documentation des traitements ;
* procédure de suppression des données personnelles ;
* justification des données utilisées.

## 9. Livrables techniques attendus

Les livrables du Bloc 1 sont :

* scripts de collecte ;
* scripts de nettoyage ;
* scripts d’agrégation ;
* fichiers bruts ;
* fichiers nettoyés ;
* dataset final ;
* scripts SQL ;
* modèle Merise ;
* base PostgreSQL ;
* script d’import ;
* API REST ;
* documentation Swagger / OpenAPI ;
* documentation technique ;
* documentation RGPD ;
* tests techniques ;
* dépôt Git versionné.

## 10. Critères de validation

Le Bloc 1 sera considéré comme validé si :

* les données sont collectées depuis plusieurs sources ;
* les scripts sont fonctionnels ;
* les erreurs et exceptions sont gérées ;
* les données brutes sont conservées ;
* les données nettoyées sont produites ;
* les règles de nettoyage sont documentées ;
* le dataset final est cohérent ;
* la base de données est créée correctement ;
* les données sont importées en base ;
* les requêtes SQL sont fonctionnelles et documentées ;
* l’API REST permet d’accéder aux données ;
* l’API est sécurisée ;
* la documentation permet de réinstaller et tester le projet ;
* le code est versionné dans Git.
