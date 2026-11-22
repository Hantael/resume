# Marine MORARD — CV as Code

[![Build and Deploy CV to GitHub Pages](https://github.com/Hantael/resume/actions/workflows/deploy.yml/badge.svg)](https://github.com/Hantael/resume/actions/workflows/deploy.yml)

CV versionné en YAML (*CV as Code*), compilé en PDF A4 ATS-friendly via [RenderCV](https://github.com/rendercv/rendercv) (Typst) et publié automatiquement en HTTPS sur GitHub Pages à chaque `git push` sur `main`.

- **CV en ligne (Vue Web + Aperçu PDF + mode clair/sombre)** : https://hantael.github.io/resume/
- **Téléchargement PDF direct (1 page A4)** : https://hantael.github.io/resume/Marine_Morard_CV.pdf

---

## Architecture

```text
Marine_Morard_CV.yaml ──▶ RenderCV (Typst) ──▶ PDF A4 + PNG HD
         │                                            │
         └──────────────▶ scripts/prepare_site.py ────┴──▶ public/ ──▶ GitHub Pages (HTTPS)
```

- **Source unique de vérité** : tout le contenu (identité, expériences, durées automatiques, compétences, formation, centres d'intérêt) vit dans [`Marine_Morard_CV.yaml`](Marine_Morard_CV.yaml).
- **Rendu PDF** : thème `engineeringclassic` (format A4, français) avec un override minimal [`engineeringclassic/entries/ExperienceEntry.j2.typ`](engineeringclassic/entries/ExperienceEntry.j2.typ) pour afficher les durées calculées automatiquement sur une seule ligne.
- **Rendu Web** : [`scripts/prepare_site.py`](scripts/prepare_site.py) génère une page statique responsive (mode clair/sombre, sélecteur Vue Web / Aperçu PDF, bouton de téléchargement PDF direct) sans dépendance frontend.
- **CI/CD** : [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) compile et déploie automatiquement sur GitHub Pages (`actions/upload-pages-artifact` + `actions/deploy-pages`).

---

## Structure du dépôt

```text
.
├── .github/workflows/deploy.yml                     # Pipeline CI/CD GitHub Actions → GitHub Pages
├── engineeringclassic/entries/ExperienceEntry.j2.typ # Override Typst (dates + durées sur 1 ligne)
├── scripts/prepare_site.py                          # Générateur HTML/CSS statique depuis le YAML
├── Marine_Morard_CV.yaml                            # Source unique du CV (RenderCV v2.8)
├── Makefile                                         # Raccourcis de build et prévisualisation locale
├── requirements.txt                                 # Dépendance Python épinglée (rendercv[full])
├── .editorconfig                                    # Conventions de formatage (UTF-8, LF, indents)
└── .gitignore
```

---

## Utilisation en local

### Prérequis
- Python 3.12+

### Commandes

```bash
# Initialiser l'environnement virtuel et installer RenderCV
make setup

# Générer le PDF (rendercv_output/) et le site statique (public/)
make build

# Prévisualiser le site web en local sur http://localhost:8000
make serve

# Nettoyer les artefacts générés
make clean
```

### Mettre à jour et redéployer

```bash
# 1. Éditer Marine_Morard_CV.yaml puis vérifier le rendu local
make build

# 2. Pousser sur main pour déclencher le déploiement GitHub Pages
git add Marine_Morard_CV.yaml
git commit -m "chore(cv): update resume"
git push origin main
```
