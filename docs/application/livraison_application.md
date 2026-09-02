# 44 — Livraison automatisée de l’application

## 1. Objectif

La livraison de l’application est automatisée après validation du packaging.

La chaîne retenue est :

```text
test
↓
build
↓
smoke test
↓
package
↓
checksum
↓
publication GHCR
↓
GitHub Release
```

La validation de l’exécution du POC dans un environnement de pré-production est traitée séparément dans C15 avec `docker-compose.preprod.yml`.

---

## 2. Déclenchement de la livraison

La livraison n’est pas exécutée à chaque push.

Elle est déclenchée uniquement lorsqu’un tag de version respectant le format sémantique est poussé :

```text
vMAJOR.MINOR.PATCH
```

Exemple :

```text
v1.0.0
```

Commandes :

```cmd
git tag v1.0.0
git push origin v1.0.0
```

Le workflow concerné est :

```text
.github/workflows/frontend_release.yml
```

---

## 3. Pourquoi utiliser un tag

Le tag permet d’identifier précisément la version livrée.

Chaque release est associée à :

```text
version
commit Git
image Docker
package Docker
checksum SHA-256
workflow GitHub Actions
```

Cette organisation permet de relier une livraison à une version exacte du dépôt.

---

## 4. Étape 1 — Test

Avant tout packaging, le workflow exécute :

```text
python -m pytest tests/test_frontend_static.py -v
```

Si les tests échouent :

```text
la chaîne s’arrête
aucune image n’est publiée
aucune GitHub Release n’est créée
```

La livraison ne peut donc avoir lieu qu’après validation des tests.

---

## 5. Étape 2 — Build Docker

Le frontend est construit à partir de :

```text
frontend/Dockerfile
```

La commande exécutée par le workflow correspond à :

```text
docker build ./frontend
```

L’image reçoit également des métadonnées OCI :

```text
source GitHub
commit Git
version
```

Ces informations renforcent la traçabilité du package.

---

## 6. Étape 3 — Smoke test du package

L’image Docker construite est démarrée temporairement dans GitHub Actions.

Le workflow vérifie ensuite que :

```text
http://127.0.0.1:8085/
```

retourne correctement le frontend.

Si le conteneur ne démarre pas ou si la page n’est pas accessible :

```text
la livraison échoue
```

L’image n’est donc pas considérée comme livrable uniquement parce que `docker build` a réussi.

---

## 7. Étape 4 — Packaging

Après validation, l’image Docker est exportée :

```text
docker save
```

puis compressée :

```text
gzip
```

Le package obtenu suit le format :

```text
paylive-frontend-v1.0.0.tar.gz
```

Ce fichier constitue une copie transportable de l’image validée.

Installation manuelle :

```cmd
docker load -i paylive-frontend-v1.0.0.tar.gz
```

---

## 8. Étape 5 — Intégrité du package

Le workflow génère :

```text
SHA256SUMS.txt
```

Le checksum SHA-256 permet de vérifier que les fichiers téléchargés n’ont pas été modifiés ou corrompus.

Exemple de contrôle sous Linux/Git Bash :

```text
sha256sum -c SHA256SUMS.txt
```

Les fichiers couverts comprennent notamment :

```text
package Docker
docker-compose.preprod.yml
env.preprod.example
RELEASE_MANIFEST.txt
```

---

## 9. Étape 6 — Publication dans GHCR

Après les tests et le packaging, l’image validée est publiée dans GitHub Container Registry.

Format :

```text
ghcr.io/<github-user>/paylive-frontend:<VERSION>
```

Exemple :

```text
ghcr.io/<github-user>/paylive-frontend:v1.0.0
```

Un second tag lie directement l’image au commit :

```text
ghcr.io/<github-user>/paylive-frontend:sha-<SHORT_SHA>
```

Le workflow utilise :

```text
GITHUB_TOKEN
```

avec :

```yaml
permissions:
  contents: write
  packages: write
```

Aucun token GHCR personnel n’est enregistré dans le dépôt.

---

## 10. Étape 7 — GitHub Release automatique

Une GitHub Release est créée automatiquement après publication de l’image.

Titre attendu :

```text
PayLive frontend v1.0.0
```

Artefacts publiés :

```text
paylive-frontend-v1.0.0.tar.gz
SHA256SUMS.txt
RELEASE_MANIFEST.txt
docker-compose.preprod.yml
env.preprod.example
```

Les notes de release rappellent :

- la version ;
- le commit ;
- l’image GHCR ;
- la chaîne de validation ;
- la commande d’installation du package.

---

## 11. Manifest de livraison

Le workflow génère :

```text
RELEASE_MANIFEST.txt
```

Il contient notamment :

```text
Application
Version
Commit
Image GHCR versionnée
Image GHCR liée au SHA
URL du workflow GitHub Actions
```

Ce fichier facilite la traçabilité entre :

```text
code source
↓
workflow
↓
package
↓
image
↓
release
```

---

## 12. Lien avec C15 — pré-production

C15 a validé une configuration de pré-production distincte :

```text
docker-compose.preprod.yml
```

avec :

```text
frontend : 8081
API      : 8001
Postgres : 5434
```

Les smoke tests de pré-production ont validé :

```text
services healthy
frontend HTTP 200
API HTTP 200
health HTTP 200
401 sans clé
403 avec clé invalide
model-info HTTP 200
prédiction IA
communication frontend/API
CORS
```

La conclusion C15 est :

```text
GO pour la validation du POC en pré-production locale conteneurisée
```

C19 complète cette validation en ajoutant une étape de **livraison automatisée et versionnée** après le packaging.

---

## 13. Chaîne complète C19

```text
Tag Git v1.0.0
↓
GitHub Actions

1. Checkout du commit tagué
↓
2. Tests frontend
↓
3. Validation du format de version
↓
4. Docker build
↓
5. Démarrage du conteneur
↓
6. Smoke test HTTP
↓
7. Docker save + gzip
↓
8. SHA-256
↓
9. Login GHCR
↓
10. Tag image v1.0.0
↓
11. Tag image sha-<commit>
↓
12. Push GHCR
↓
13. Génération des notes
↓
14. Création GitHub Release
↓
15. Publication des artefacts
```

---

## 14. Conditions d’échec

La Release ne doit pas être créée si :

- les tests échouent ;
- le tag ne respecte pas `vMAJOR.MINOR.PATCH` ;
- le build Docker échoue ;
- le smoke test échoue ;
- le packaging échoue ;
- la publication GHCR échoue.

La GitHub Release représente donc un package ayant franchi les étapes de validation précédentes.

---

## 15. Preuves C19 à conserver

Captures recommandées après la première exécution réelle :

```text
preuve_c19_tag_v1.0.0.png
preuve_c19_actions_release_green.png
preuve_c19_test_frontend.png
preuve_c19_docker_build.png
preuve_c19_smoke_test.png
preuve_c19_ghcr_image.png
preuve_c19_github_release.png
preuve_c19_release_assets.png
preuve_c19_sha256.png
```

Conserver également :

```text
.github/workflows/frontend_release.yml
URL GitHub Release
tag Git
SHA commit
nom image GHCR
RELEASE_MANIFEST.txt
SHA256SUMS.txt
```

---

## 16. Procédure de première livraison

Avant de créer le tag, vérifier l’état Git :

```cmd
git status
```

Committer les fichiers C19 :

```cmd
git add .github\workflows\frontend_release.yml
git add docs\08_application\44_livraison_application.md
git add docker-compose.preprod.yml
git add .env.preprod.example
git commit -m "Add automated frontend delivery workflow"
git push
```

Créer ensuite la version :

```cmd
git tag v1.0.0
git push origin v1.0.0
```

Sur GitHub :

```text
Actions
→ Frontend Release
```

Attendre que le workflow termine.

Puis vérifier :

```text
GitHub repository
→ Releases
→ v1.0.0
```

et :

```text
GitHub repository
→ Packages
→ paylive-frontend
```

---

## 17. Validation finale C19

À remplir uniquement après l’exécution réelle.

```text
Version livrée :
À renseigner

Tag :
À renseigner

Commit :
À renseigner

Workflow :
À renseigner

Tests :
PASS / FAIL

Build :
PASS / FAIL

Smoke test :
PASS / FAIL

Packaging :
PASS / FAIL

Checksum :
PASS / FAIL

Push GHCR :
PASS / FAIL

GitHub Release :
PASS / FAIL

Conclusion C19 :
VALIDÉE / NON VALIDÉE
```

C19 ne doit être déclarée totalement validée qu’après une exécution réelle et réussie du workflow de Release.
