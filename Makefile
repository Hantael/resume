.DEFAULT_GOAL := help

PYTHON ?= python3
VENV := .venv
VENV_BIN := $(VENV)/bin
CV_FILE := Marine_Morard_CV.yaml
PORT ?= 8000

.PHONY: help setup render build serve clean

help: ## Afficher les commandes disponibles
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

setup: ## Créer le virtualenv et installer les dépendances
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt

render: ## Compiler uniquement les artefacts RenderCV (PDF, PNG, Typst)
	$(VENV_BIN)/rendercv render $(CV_FILE)

build: clean render ## Compiler le CV et assembler le dossier public/ pour GitHub Pages
	$(VENV_BIN)/python scripts/prepare_site.py

serve: ## Servir public/ localement sur http://localhost:$(PORT)
	$(PYTHON) -m http.server $(PORT) --directory public

clean: ## Supprimer les artefacts générés localement
	rm -rf rendercv_output public
