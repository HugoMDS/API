#!/bin/bash

# Installer les dépendances
pip3 install -r requirements.txt

# Démarrer l'application Flask
gunicorn app:app