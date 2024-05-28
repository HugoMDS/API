#!/bin/bash

# Installer les dépendances
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Démarrer l'application Flask
exec gunicorn app:app --bind 0.0.0.0:5000 --workers 3
