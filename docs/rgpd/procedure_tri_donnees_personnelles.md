# Procédure de tri des données personnelles et mise en conformité RGPD

## 1. Objet du document

Cette procédure décrit les règles de tri, de contrôle, de minimisation, de pseudonymisation, de conservation et de suppression des données à caractère personnel susceptibles d'être manipulées par le projet.

Elle complète le registre de traitement et la documentation RGPD du projet. Son objectif est de définir, pour chaque catégorie de données, les traitements à appliquer ainsi que leur fréquence d'exécution afin de garantir qu'une future utilisation de données réelles reste conforme aux principes de protection des données.

> **Important — périmètre actuel du POC**
>
> Le POC actuel n'utilise **aucune donnée réelle PayLive**. Les données manipulées sont simulées, fictives ou pseudonymisées. Les identités, emails, numéros de téléphone, usernames, commentaires, commandes et références de paiement présents dans le projet ont uniquement un rôle de démonstration technique.
>
> La présente procédure formalise cependant le processus qui devrait être appliqué si le projet devait évoluer vers l'utilisation de données réelles provenant de vendeurs ou d'utilisateurs de la plateforme.

---

## 2. Principes de traitement retenus

La procédure s'appuie sur les principes suivants :

- **minimisation** : ne conserver que les données strictement nécessaires à la finalité du traitement ;
- **finalité déterminée** : chaque donnée doit avoir un usage métier ou technique explicite ;
- **exactitude** : les données utilisées doivent être contrôlées et corrigées si nécessaire ;
- **limitation de conservation** : aucune donnée personnelle ne doit être conservée sans durée définie ;
- **pseudonymisation** : les identifiants directement liés à une personne doivent être remplacés ou transformés lorsque leur présence n'est pas nécessaire ;
- **contrôle d'accès** : l'accès aux données doit être limité aux composants et utilisateurs autorisés ;
- **traçabilité** : les opérations importantes de tri, import, correction et suppression doivent pouvoir être documentées ;
- **privacy by design** : les traitements sont conçus pour limiter l'exposition des données dès la conception du pipeline.

---

## 3. Catégories de données personnelles concernées

Dans une future version alimentée par des données réelles, les catégories suivantes pourraient être concernées :

| Catégorie | Exemples | Niveau de sensibilité dans le projet |
|---|---|---|
| Identité vendeur | prénom, nom, nom de boutique | donnée personnelle |
| Coordonnées vendeur | email, téléphone | donnée personnelle directe |
| Identité client | username, identifiant plateforme | donnée personnelle ou pseudonyme |
| Coordonnées client | email | donnée personnelle directe |
| Commentaires | texte publié pendant un live | contenu potentiellement personnel |
| Données d'achat | panier, commande, produit, montant | donnée comportementale / transactionnelle |
| Données de paiement | statut, fournisseur, référence de transaction | donnée transactionnelle ; aucune donnée bancaire complète ne doit être stockée |
| Données techniques | événements, logs, erreurs, timestamps | potentiellement rattachables à un utilisateur |
| Prédictions IA | intention prédite, score de confiance | donnée dérivée |

Dans le POC actuel, ces données sont **simulées** et ne permettent pas d'identifier une personne réelle.

---

## 4. Procédure générale de tri

Le tri est réalisé à plusieurs moments du cycle de traitement afin d'éviter qu'une donnée inutile ou non conforme ne soit propagée jusqu'à la base finale.

### 4.1. Étape 1 — Contrôle à la collecte

À chaque collecte, les données doivent être comparées avec la liste des champs autorisés.

Les champs qui ne sont pas nécessaires au projet doivent être supprimés avant leur sauvegarde dans les zones de traitement.

Exemples :

- ne pas collecter une adresse postale si elle n'est pas nécessaire ;
- ne pas collecter de numéro de carte bancaire ;
- ne pas conserver un token d'authentification dans les fichiers de données ;
- ne pas recopier inutilement des informations personnelles dans plusieurs tables.

**Fréquence : à chaque exécution du pipeline de collecte.**

### 4.2. Étape 2 — Détection des données personnelles

Les colonnes et contenus textuels doivent être contrôlés afin d'identifier les données personnelles directes ou indirectes.

Les contrôles peuvent porter sur :

- emails ;
- numéros de téléphone ;
- noms et prénoms ;
- usernames ;
- identifiants externes ;
- commentaires contenant potentiellement des informations personnelles ;
- références de transaction.

**Fréquence : à chaque nouveau lot de données et avant import dans la zone `processed`.**

### 4.3. Étape 3 — Minimisation

Toute colonne ne contribuant pas directement au besoin fonctionnel, analytique, IA, de sécurité ou d'audit doit être exclue du dataset utilisé.

Le principe est de ne pas transmettre à la couche suivante plus de données que nécessaire.

**Fréquence : à chaque évolution de schéma et à chaque nouvelle source de données.**

### 4.4. Étape 4 — Pseudonymisation

Les identifiants directs doivent être remplacés lorsque leur valeur réelle n'est pas nécessaire.

Exemples :

- remplacement d'un `customer_id` réel par un identifiant technique interne ;
- hachage ou tokenisation d'un identifiant externe ;
- suppression du prénom et du nom lors de la création d'un dataset IA ;
- utilisation d'un identifiant de session à la place d'un identifiant personnel.

**Fréquence : à chaque import contenant des données personnelles réelles.**

### 4.5. Étape 5 — Suppression ou masquage

Une donnée doit être supprimée ou masquée lorsqu'elle :

- n'est plus nécessaire à la finalité prévue ;
- dépasse sa durée de conservation ;
- a été collectée par erreur ;
- contient une information interdite ou excessive ;
- fait l'objet d'une demande valide de suppression.

**Fréquence : contrôle automatisé mensuel, et immédiatement en cas de demande ou d'incident.**

---

## 5. Matrice des traitements et fréquences

| Donnée / catégorie | Traitement à appliquer | Fréquence |
|---|---|---|
| `seller_id` | pseudonymisation si identifiant externe réel | à chaque import |
| `customer_id` | pseudonymisation / remplacement par identifiant interne | à chaque import |
| prénom / nom vendeur | conservation uniquement si nécessaire ; sinon suppression | à chaque import et revue trimestrielle |
| email vendeur | validation, minimisation, masquage dans les exports | à chaque import |
| téléphone vendeur | validation, minimisation ou suppression si non nécessaire | à chaque import |
| username client | pseudonymisation si identification directe possible | à chaque import |
| email client | suppression du dataset IA ; conservation uniquement si finalité justifiée | à chaque préparation de dataset |
| commentaires | contrôle de données personnelles, nettoyage, minimisation | à chaque préparation NLP |
| texte destiné à l'IA | suppression des identifiants directs inutiles | à chaque génération du dataset IA |
| montant panier / commande | conservation si nécessaire à l'analyse métier | à chaque import |
| référence de transaction | pseudonymisation / masquage | à chaque import |
| données bancaires complètes | **interdiction de collecte et de stockage** | contrôle permanent |
| logs applicatifs | éviter les secrets et données personnelles inutiles | à chaque génération de log |
| logs de prédictions IA | conserver uniquement les champs nécessaires au monitoring | à chaque prédiction |
| fichiers temporaires | suppression après validation du traitement | après chaque batch |
| exports de test | contrôle et suppression après usage | après chaque campagne de test |
| données dépassant la durée de conservation | suppression ou anonymisation | mensuel |
| structure des données collectées | revue de minimisation | à chaque nouvelle source |
| registre RGPD | mise à jour en cas de nouveau traitement | à chaque changement majeur et revue annuelle |

---

## 6. Traitement spécifique des commentaires de live

Les commentaires représentent une catégorie importante car ils peuvent contenir du texte libre.

Dans une version réelle, un utilisateur pourrait saisir volontairement ou involontairement :

- son nom ;
- son numéro de téléphone ;
- une adresse ;
- un email ;
- une information privée ;
- une référence de commande.

Avant leur utilisation pour l'entraînement ou l'évaluation d'un modèle, les commentaires doivent donc être nettoyés afin de supprimer ou masquer les éléments permettant une identification directe.

Exemple :

```text
Entrée réelle :
"Je suis Marie Dupont, appelez-moi au 06 XX XX XX XX pour la robe noire"

Version destinée au dataset IA :
"Je souhaite être contacté pour la robe noire"
```

Le commentaire nettoyé conserve l'information utile à la classification tout en retirant les données personnelles inutiles.

**Fréquence : à chaque préparation ou réentraînement du dataset NLP.**

---

## 7. Traitement des données de paiement

Le projet ne doit pas stocker :

- numéro complet de carte bancaire ;
- cryptogramme ;
- identifiants bancaires complets ;
- données d'authentification bancaire.

Seules des informations techniques ou métier peuvent être conservées si elles sont nécessaires :

- statut du paiement ;
- montant ;
- devise ;
- fournisseur ;
- méthode de paiement ;
- référence technique pseudonymisée.

Dans le POC actuel, toutes ces informations sont simulées.

**Fréquence du contrôle : à chaque import de données de paiement et à chaque évolution du schéma `payments`.**

---

## 8. Traitement des logs et données de monitoring

Les logs ne doivent jamais devenir une copie incontrôlée des données métier.

Avant journalisation, il faut vérifier que les logs ne contiennent pas :

- clé API ;
- mot de passe ;
- token ;
- email complet inutile ;
- numéro de téléphone ;
- données bancaires ;
- commentaire complet si ce contenu n'est pas nécessaire au diagnostic.

Pour le monitoring IA, les champs conservés doivent être limités aux informations utiles, par exemple :

- timestamp ;
- intention prédite ;
- score de confiance ;
- temps de réponse ;
- version du modèle ;
- type d'alerte.

Si le texte complet du commentaire doit être conservé pour analyser une erreur du modèle, cette conservation doit être justifiée, limitée et protégée.

**Fréquence : contrôle à chaque évolution du système de logging et revue mensuelle des fichiers de monitoring.**

---

## 9. Durées de conservation proposées pour une future version réelle

Les durées suivantes constituent des règles de conception pour une future version utilisant des données réelles. Elles devront être validées juridiquement avant mise en production.

| Type de donnée | Durée indicative | Action à échéance |
|---|---:|---|
| données brutes temporaires | 30 jours | suppression |
| données intermédiaires | 90 jours | suppression ou anonymisation |
| commentaires utilisés pour analyse | durée minimale nécessaire | anonymisation / suppression |
| dataset IA anonymisé | selon besoin de réentraînement | revue régulière |
| logs techniques | 90 jours | rotation / suppression |
| logs de monitoring IA | 6 mois maximum si nécessaire | suppression ou agrégation |
| exports de tests | durée de la campagne | suppression immédiate après validation |
| données d'audit | selon obligations applicables | archivage contrôlé |

Ces durées sont indicatives et doivent être ajustées à la finalité réelle, aux obligations contractuelles et aux exigences réglementaires.

---

## 10. Procédure de suppression

Lorsqu'une suppression est nécessaire, elle doit être appliquée dans toutes les zones où la donnée est présente.

Ordre recommandé :

1. identifier la donnée et son identifiant technique ;
2. rechercher ses occurrences dans les données brutes, intermédiaires et finales ;
3. supprimer ou anonymiser la donnée dans PostgreSQL ;
4. supprimer les fichiers temporaires concernés ;
5. vérifier les logs et exports ;
6. vérifier si la donnée est incluse dans un dataset IA ;
7. régénérer le dataset si nécessaire ;
8. tracer l'opération de suppression dans un journal d'audit.

Dans une future version réelle, une procédure automatisée devrait être privilégiée afin de réduire le risque d'oubli.

---

## 11. Gestion des demandes d'exercice de droits

Si des données réelles sont utilisées, les demandes d'accès, rectification, opposition ou suppression doivent pouvoir être traitées.

La procédure cible serait :

1. réception de la demande ;
2. vérification de l'identité du demandeur selon la procédure définie ;
3. recherche des données concernées ;
4. application de la demande ;
5. contrôle des copies ou datasets dérivés ;
6. traçabilité de l'action ;
7. réponse au demandeur dans le délai réglementaire applicable.

**Fréquence : à chaque demande reçue.**

---

## 12. Contrôles avant mise en production

Avant toute utilisation de données réelles, les contrôles suivants doivent être réalisés :

- validation du registre des traitements ;
- validation de la finalité de chaque donnée collectée ;
- vérification des durées de conservation ;
- revue du schéma de base de données ;
- vérification des données envoyées au modèle IA ;
- vérification des logs ;
- contrôle des accès ;
- test de la procédure de suppression ;
- test de pseudonymisation ;
- vérification du `.gitignore` et des secrets ;
- validation juridique ou DPO si nécessaire.

Aucune donnée réelle ne doit être introduite dans le système tant que ces vérifications ne sont pas terminées.

---

## 13. Application au POC actuel

Dans l'état actuel du projet :

- les données sont simulées ;
- les identités sont fictives ;
- les commentaires sont artificiels ;
- les références de transaction sont fictives ;
- aucune donnée bancaire réelle n'est stockée ;
- aucune donnée réelle issue de PayLive n'est intégrée ;
- les traitements RGPD sont donc documentés principalement comme préparation à une future mise en production.

Cette procédure constitue une **règle cible** pour l'évolution du POC.

Si le modèle est ultérieurement intégré directement à la plateforme et traite les commentaires réels des vendeurs en live, cette procédure devra être activée dans le pipeline de données et complétée par les validations juridiques et organisationnelles nécessaires.

---

## 14. Fréquences de contrôle récapitulatives

| Contrôle | Fréquence |
|---|---|
| contrôle des champs collectés | à chaque collecte |
| validation des données personnelles | à chaque lot |
| pseudonymisation | à chaque import réel |
| nettoyage des commentaires | à chaque préparation NLP |
| contrôle des logs | à chaque évolution + revue mensuelle |
| suppression des fichiers temporaires | après chaque batch |
| purge des données arrivées à échéance | mensuelle |
| revue de minimisation | à chaque nouvelle source |
| mise à jour du registre RGPD | à chaque nouveau traitement |
| revue générale RGPD | annuelle minimum |
| traitement d'une demande de suppression | à chaque demande |
| contrôle avant mise en production | avant chaque mise en production majeure |

---

## 15. Traçabilité et versionnement

Cette procédure doit être versionnée dans le même dépôt Git que le reste du projet :

```text
docs/rgpd/procedure_tri_donnees_personnelles.md
```

Toute modification importante du pipeline de données, du schéma PostgreSQL, du dataset IA ou du système de monitoring doit déclencher une revue de cette procédure.

Exemples de modifications nécessitant une revue :

- ajout d'une nouvelle source de données ;
- ajout d'une nouvelle donnée personnelle ;
- intégration de données réelles ;
- ajout d'un fournisseur externe ;
- ajout de nouvelles informations dans les logs ;
- changement de durée de conservation ;
- changement de finalité du traitement.

---

## 16. Conclusion

La procédure de tri constitue un garde-fou avant toute utilisation de données personnelles réelles. Elle définit les opérations de contrôle, minimisation, pseudonymisation et suppression ainsi que leur fréquence d'exécution.

Dans le POC actuel, les données sont entièrement simulées. Cette procédure n'est donc pas utilisée pour traiter des personnes réelles, mais elle formalise le fonctionnement attendu si la solution évolue vers une intégration avec des données réelles.

Elle permet ainsi de préparer l'évolution du projet vers un contexte d'exploitation réel tout en conservant une approche structurée, documentée et compatible avec les principes du RGPD.
