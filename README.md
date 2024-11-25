# Gestion Automatique du Programme des Chauffeurs

## Description du Projet  
Ce projet a pour objectif de fournir un **outil de gestion automatisée du programme des chauffeurs** qui permet de :  
* **Optimiser les plannings des chauffeurs** (journalier, hebdomadaire, mensuel).  
* **Maximiser le nombre de courses réalisées** par jour.  
* **Minimiser le nombre de chauffeurs à embaucher**, tout en respectant les contraintes légales et organisationnelles.  

## Fonctionnalités  
### Volet Prévision  
Le volet prévision consiste à :  
1. Prévoir le nombre de courses futures sur une période de deux semaines.  
2. Utiliser l'algorithme de machine learning **Prophet** développé par Facebook.  
3. Basé sur la colonne `At Pickup Time` des données historiques, les prévisions sont effectuées pour trois tranches horaires :  
   - 6h-14h  
   - 14h-23h  
   - 23h-5h  

#### Étapes pour Exécuter les Prévisions  
1. Accéder au répertoire de préparation des données :  
   ```bash
    cd timefold-quickstarts/python/prevision/src/data_preparation
2. Le fichier prétraité sera stocké dans : timefold-quickstarts/python/prevision/preprocessing
    ```bash
    python feature_store.py 
3. Les prévisions seront stockées dans : timefold-quickstarts/python/prevision/prediction_train, les détails des modèles seront disponibles dans : timefold-quickstarts/python/prevision/training_models 
    ```bash
    python train_mult.py 


### Volet Outil de Planification
#### Étapes pour Démarrer
1. Configurer l'environnement virtuel :
    ```bash
    cd timefold-quickstarts/python/employee-scheduling
    python -m venv .venv
    . .venv/bin/activate
    pip install -e .
2. Charger les prévisions réalisées par le modèle pour définir le nombre de tâches à effectuer.


#### Fonctionnalités
- Ajouter une liste personnalisable des chauffeurs depuis un fichier .txt ou via des paramètres dans le module demo_data.
- Gérer les disponibilités des chauffeurs :
    * Périodes où les chauffeurs souhaitent travailler.
    * Périodes d'indisponibilité.
    * Contraintes personnelles.

#### Contraintes Définies
- Un chauffeur dispose de deux jours de repos par semaine (cinq jours de travail).
- Un chauffeur ne doit pas enchaîner trois nuits de travail consécutives.
- Un chauffeur travaille 10 heures maximum par jour.
- Les horaires de nuit sont définis légalement de 23h à 5h.

#### Résolution et Visualisation
Le solver attribue les chauffeurs aux différentes tâches en prenant en compte les contraintes définies.

#### Étapes pour Visualiser la Planification
Lancer le serveur FastAPI :
    ```bash
    cd timefold-quickstarts/python/employee-scheduling
    run-app
Accéder à l’interface de planification via :
    http://127.0.0.1:8080

#### Captures d'Écran
Des captures d'écran de l'interface et des résultats seront incluses dans le rendu final pour illustrer le fonctionnement.

#### Technologies Utilisées
Python
Framework Timefold
Machine Learning avec Facebook Prophet
FastAPI

## Auteur
GUINDO HUSSEN HUGUES JUNIOR