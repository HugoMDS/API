#!/bin/bash

# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'application Flask
gunicorn app:app