# 30b — Livraison continue et déploiement du modèle IA

## 1. Objectif

Cette documentation complète la chaîne MLOps en ajoutant les étapes de **packaging et de déploiement du modèle**.

Avant cette évolution, le workflow automatisait déjà :

```text
préparation du dataset
↓
entraînement
↓
benchmark
↓
monitoring
↓
tests automatisés
↓
validation du frontend Docker
```

La chaîne est désormais étendue avec :

```text
tests et validation
↓
vérification des artefacts du modèle
↓
docker build API + modèle
↓
smoke test local de l'image
↓
docker tag
↓
authentification GHCR
↓
docker push
↓
pull de l'image publiée
↓
déploiement éphémère dans le runner CI
↓
smoke test de l'image publiée
```

Le modèle n'est donc plus uniquement généré sous forme de fichiers locaux : il est inclus dans une image Docker versionnée, publiée dans GitHub Container Registry et redéployée dans un environnement de validation.

---

## 2. Artefacts du modèle

L'entraînement produit les fichiers suivants :

```text
models/intent_classifier/model.joblib
models/intent_classifier/vectorizer.joblib
models/intent_classifier/label_encoder.joblib
models/intent_classifier/model_metadata.json
```

Le workflow vérifie explicitement leur présence avant le packaging.

Si un artefact manque, le job GitHub Actions échoue avant la création de l'image de livraison.

---

## 3. Image de livraison

L'image construite regroupe :

- l'API FastAPI ;
- le code d'inférence ;
- les dépendances Python ;
- les artefacts entraînés du modèle ;
- les métadonnées nécessaires à la restitution de la version du modèle.

Nom local utilisé dans la CI :

```text
paylive-ai-api:ci
```

Nom publié :

```text
ghcr.io/<proprietaire-github>/paylive-ai-api
```

Deux tags sont créés lors d'un push sur la branche principale :

```text
latest
<GITHUB_SHA>
```

Exemple :

```text
ghcr.io/mon-compte/paylive-ai-api:latest
ghcr.io/mon-compte/paylive-ai-api:8e12f4...
```

Le tag basé sur le SHA Git apporte une traçabilité entre :

```text
code source
↕
commit Git
↕
modèle entraîné
↕
image Docker publiée
```

---

## 4. Déclenchement

Le workflow reste déclenché sur :

```text
push main/master
pull_request main/master
workflow_dispatch
```

La construction et le smoke test local sont exécutés pendant la validation du pipeline.

La publication GHCR est autorisée dans deux cas :

```text
push sur main/master
workflow_dispatch lancé sur main/master
```

Les Pull Requests ne publient pas d'image dans le registre. Un lancement manuel sur une autre branche construit et teste l'image mais ne la publie pas.

---

## 5. Permissions GitHub Actions

Le workflow définit :

```yaml
permissions:
  contents: read
  packages: write
```

`contents: read` permet au workflow de lire le dépôt.

`packages: write` permet au `GITHUB_TOKEN` du workflow de publier l'image dans GitHub Container Registry.

Aucun mot de passe GHCR n'est inscrit directement dans le dépôt.

Authentification :

```text
registry : ghcr.io
username : github.actor
password : secrets.GITHUB_TOKEN
```

---

## 6. Vérification avant packaging

Avant le `docker build`, le workflow vérifie :

```text
model.joblib
vectorizer.joblib
label_encoder.joblib
model_metadata.json
```

Cette étape garantit que l'image construite correspond bien à un modèle entraîné dans la même exécution du pipeline.

---

## 7. Packaging Docker

Commande logique utilisée :

```bash
docker build \
  --label "org.opencontainers.image.source=https://github.com/${GITHUB_REPOSITORY}" \
  --label "org.opencontainers.image.revision=${GITHUB_SHA}" \
  -t paylive-ai-api:ci \
  .
```

Les labels OCI apportent des informations de traçabilité sur :

- le dépôt source ;
- le commit associé à l'image.

Après le build, le workflow démarre un conteneur temporaire et vérifie que les artefacts du modèle existent bien dans :

```text
/app/models/intent_classifier/
```

Le packaging est donc validé avant toute publication.

---

## 8. Smoke test avant publication

L'image locale est démarrée dans le runner GitHub Actions :

```text
paylive-ai-api:ci
```

Commande de service :

```text
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Le workflow attend que l'API réponde puis vérifie :

```text
GET /health
```

Résultat attendu :

```text
HTTP 200
```

Ensuite :

```text
GET /api/v1/ai/model-info
X-API-Key: paylive-dev-api-key
```

Résultat attendu :

```text
HTTP 200
```

Le deuxième test est important : il vérifie non seulement que le serveur démarre, mais également que le service IA peut charger les informations du modèle inclus dans l'image.

---

## 9. Tag de l'image

Après validation locale :

```bash
docker tag paylive-ai-api:ci ghcr.io/<owner>/paylive-ai-api:latest
docker tag paylive-ai-api:ci ghcr.io/<owner>/paylive-ai-api:<GITHUB_SHA>
```

Le tag `latest` représente la dernière version livrée depuis la branche principale.

Le tag `<GITHUB_SHA>` représente une version immuable et traçable.

---

## 10. Publication dans GitHub Container Registry

Le workflow s'authentifie à :

```text
ghcr.io
```

puis exécute :

```bash
docker push ghcr.io/<owner>/paylive-ai-api:latest
docker push ghcr.io/<owner>/paylive-ai-api:<GITHUB_SHA>
```

Le package devient visible dans la section **Packages** du compte ou de l'organisation GitHub.

La publication dans GHCR constitue l'étape de distribution du modèle packagé.

---

## 11. Déploiement de validation

Après publication, le workflow récupère explicitement l'image versionnée :

```bash
docker pull ghcr.io/<owner>/paylive-ai-api:<GITHUB_SHA>
```

Cette image issue du registre est ensuite démarrée dans un nouveau conteneur du runner GitHub Actions.

Cette étape constitue un **déploiement éphémère en environnement de validation CI** :

```text
GHCR
↓
docker pull
↓
conteneur temporaire
↓
API démarrée
↓
modèle chargé
↓
smoke tests
```

Elle permet de vérifier que l'artefact réellement publié est réutilisable indépendamment du workspace de build.

---

## 12. Smoke test après déploiement

Les mêmes contrôles sont appliqués à l'image récupérée depuis GHCR :

```text
GET /health → 200
```

et :

```text
GET /api/v1/ai/model-info
X-API-Key: paylive-dev-api-key
→ 200
```

La réponse `model-info` est enregistrée dans :

```text
model_info_smoke_ghcr.json
```

Ce fichier est ajouté aux artefacts du workflow et sert de preuve que le modèle packagé et publié peut être redéployé.

---

## 13. Comportement selon l'événement Git

| Événement | Tests | Build API + modèle | Smoke local | Push GHCR | Smoke image publiée |
|---|---:|---:|---:|---:|---:|
| Pull Request | oui | oui | oui | non | non |
| Push main/master | oui | oui | oui | oui | oui |
| workflow_dispatch sur main/master | oui | oui | oui | oui | oui |
| workflow_dispatch sur autre branche | oui | oui | oui | non | non |

Cette séparation évite de publier des images pour chaque Pull Request.

---

## 14. Vérification locale avant commit

Avant d'envoyer la modification du workflow :

```cmd
pytest tests\test_ai_dataset.py tests\test_intent_model.py tests\test_ai_api.py tests\test_frontend_static.py -v
```

Puis :

```cmd
python src\ai\data_preparation\prepare_nlp_dataset.py
python src\ai\training\train_intent_classifier.py
```

Vérifier les artefacts :

```cmd
dir models\intent_classifier
```

Construire l'image :

```cmd
docker build -t paylive-ai-api:c13 .
```

Vérifier le contenu packagé :

```cmd
docker run --rm --entrypoint sh paylive-ai-api:c13 -c "ls -la /app/models/intent_classifier"
```

Démarrer l'image :

```cmd
docker run -d --name paylive_ai_c13 -p 8010:8000 -e API_KEY=paylive-dev-api-key paylive-ai-api:c13 python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Tester :

```cmd
curl -i http://127.0.0.1:8010/health
```

Puis :

```cmd
curl -i -H "X-API-Key: paylive-dev-api-key" http://127.0.0.1:8010/api/v1/ai/model-info
```

Nettoyage :

```cmd
docker rm -f paylive_ai_c13
```

---

## 15. Installation du workflow dans le dépôt

Le fichier final doit remplacer :

```text
.github/workflows/ai_mlops_ci.yml
```

Sous Windows CMD, depuis la racine :

```cmd
copy ai_mlops_ci_c13_ghcr.yml .github\workflows\ai_mlops_ci.yml
```

Puis :

```cmd
git diff -- .github\workflows\ai_mlops_ci.yml
```

Vérifier ensuite :

```cmd
git status
```

Commit :

```cmd
git add .github\workflows\ai_mlops_ci.yml
git add docs\ai_service\30b_livraison_continue_modele.md
git commit -m "Add model packaging and GHCR delivery pipeline"
```

Push :

```cmd
git push
```

Le push déclenche le workflow sur `main` ou `master`.

---

## 16. Vérification sur GitHub

Dans GitHub :

```text
Repository
→ Actions
→ AI MLOps CI
```

Les étapes C13 attendues sont :

```text
Verify trained model artifacts
Build API image with packaged model
Verify model is packaged in Docker image
Smoke test packaged image locally
Log in to GitHub Container Registry
Tag API image for GHCR
Push API image to GHCR
Pull published image from GHCR
Smoke test published GHCR image
```

Toutes doivent être vertes sur un push de la branche principale.

---

## 17. Vérification du package GHCR

Après le premier push réussi :

```text
GitHub
→ profil / organisation
→ Packages
→ paylive-ai-api
```

Vérifier la présence de :

```text
latest
commit SHA
```

La page du package constitue une preuve du packaging et de la publication.

---

## 18. Cas d'échec GHCR

### 18.1. Permission refusée

Si le workflow retourne une erreur de type :

```text
permission_denied
denied
403
```

vérifier :

```yaml
permissions:
  contents: read
  packages: write
```

Vérifier également les paramètres GitHub Actions du dépôt et l'accès du dépôt au package.

### 18.2. Package déjà existant mais non lié au dépôt

Si un package du même nom avait été créé auparavant manuellement, il peut ne pas être lié au dépôt.

Dans ce cas :

```text
Package
→ Package settings
→ Manage Actions access
```

ajouter le dépôt courant si nécessaire.

### 18.3. Smoke test échoue sur model-info

Consulter les logs du step :

```text
Smoke test published GHCR image
```

Le workflow affiche les logs Docker avant de supprimer le conteneur.

Vérifier notamment :

- présence des fichiers `joblib` ;
- chemin `/app/models/intent_classifier` ;
- dépendances Python ;
- valeur `API_KEY` ;
- démarrage Uvicorn.

---

## 19. Preuves à conserver pour C13

Captures recommandées :

```text
preuve_c13_pipeline_actions_vert.png
preuve_c13_build_api_modele.png
preuve_c13_ghcr_push.png
preuve_c13_package_ghcr.png
preuve_c13_tags_latest_sha.png
preuve_c13_pull_image_publiee.png
preuve_c13_smoke_health.png
preuve_c13_smoke_model_info.png
```

Captures particulièrement fortes :

1. workflow complet vert ;
2. étape `Push API image to GHCR` ;
3. page GitHub Packages avec l'image ;
4. tags `latest` et SHA ;
5. étape `Smoke test published GHCR image` ;
6. contenu de `model_info_smoke_ghcr.json`.

---

## 20. Traçabilité

La chaîne finale est :

```text
dataset versionné
↓
entraînement automatique
↓
modèle et métadonnées
↓
tests automatiques
↓
image Docker contenant le modèle
↓
tag latest + SHA Git
↓
publication GHCR
↓
pull de l'image publiée
↓
déploiement temporaire dans le runner
↓
health check
↓
validation model-info
```

Cette chaîne associe donc une version du code, une version du modèle et une version de l'image livrée.

---

## 21. Limites et évolution vers la production

Le déploiement réalisé par cette chaîne est un déploiement de validation dans l'environnement CI. Il prouve que l'image publiée est récupérable et exécutable.

Le POC ne déploie pas encore automatiquement le service vers un serveur de production permanent.

Une évolution ultérieure pourrait ajouter :

```text
GHCR
↓
staging
↓
smoke tests
↓
validation
↓
production
```

avec un environnement GitHub protégé, une authentification plus robuste, HTTPS, une gestion centralisée des secrets et une procédure de rollback.

---

## 22. Conclusion

La chaîne MLOps ne s'arrête plus aux tests et à la génération des artefacts du modèle.

Le modèle est désormais prévu pour être packagé avec son API dans une image Docker, versionné par commit Git, publié dans GitHub Container Registry puis redéployé dans un environnement de validation afin d'exécuter des smoke tests sur l'artefact réellement livré.

Cette évolution apporte les étapes de packaging, livraison, déploiement de validation et contrôle post-déploiement nécessaires pour démontrer une chaîne de livraison continue du modèle.
