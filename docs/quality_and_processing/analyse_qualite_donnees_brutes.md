# Analyse de la qualité des données brutes — Bloc 1

## 1. Objectif

L’objectif de cette étape est d’analyser la qualité des données brutes avant toute opération de nettoyage.

Cette analyse permet d’identifier les anomalies présentes dans les fichiers sources et de justifier les règles de nettoyage appliquées dans les étapes suivantes.

## 2. Script utilisé

Le script utilisé est :

`src/data_processing/analyze_raw_data_quality.py`

Il lit les fichiers présents dans le dossier `data/raw` et produit trois rapports dans le dossier `data/interim`.

## 3. Rapports générés

Les rapports générés sont :

- `quality_report_files.csv` : synthèse de qualité par fichier ;
- `quality_report_columns.csv` : analyse détaillée par colonne ;
- `quality_report_business_rules.csv` : anomalies détectées selon les règles métier.

## 4. Types d’anomalies contrôlées

Les contrôles réalisés portent sur :

- valeurs manquantes ;
- lignes dupliquées ;
- identifiants dupliqués ;
- dates invalides ;
- emails invalides ;
- valeurs numériques invalides ;
- montants négatifs ;
- statuts non autorisés ;
- plateformes non normalisées ;
- devises incorrectes ;
- références inexistantes entre fichiers ;
- incohérences temporelles ;
- incohérences de calcul.

## 5. Utilité pour le projet

Cette analyse sert de base à la définition des règles de nettoyage.

Elle permet de démontrer que les données ne sont pas transformées arbitrairement, mais à partir d’un diagnostic clair et documenté.

## 6. Sorties produites

Les fichiers de sortie sont stockés dans :

`data/interim`

Ces fichiers sont considérés comme des livrables intermédiaires et peuvent être utilisés comme preuves dans le rapport professionnel.

## 7. Conclusion

L’analyse de qualité des données brutes confirme la présence d’anomalies volontaires dans les datasets simulés.

Ces anomalies permettront de mettre en œuvre les traitements de nettoyage, normalisation et agrégation nécessaires à la construction du dataset final.