# Projet Finance - Dashboard Institutionnel

Ce projet est une plateforme d'analyse financière développée en Python (Streamlit) et déployée sur un serveur AWS. Il permet d'analyser des actifs individuels et de gérer des portefeuilles multi-actifs.

## Lien de l'application (Live 24/7)
L'application est hébergée sur une instance AWS EC2 et reste accessible en permanence ici :
 **http://56.228.36.12:8501**

## Fonctionnalités du Dashboard

### Partie A : Analyse d'Action Unique (Quant A)
* **Données en temps réel** : Récupération automatique via l'API Yahoo Finance.
* **Stratégies de Trading** : Implémentation des signaux SMA Crossover et RSI.
* **Indicateurs clés** : Calcul du Max Drawdown et du **Sharpe Ratio** :
  $$Sharpe = \frac{R_p - R_f}{\sigma_p}$$
* **Bonus IA** : Modèle de Régression Linéaire pour prédire les prix sur les 5 prochains jours.

### Partie B : Gestion de Portefeuille (Quant B)
* **Multi-actifs** : Simulation sur un panier d'au moins 3 actions (ex: AAPL, NVDA, TSLA).
* **Analyse du Risque** : Affichage d'une matrice de corrélation interactive.
* **Optimisation** : Visualisation de l'effet de diversification sur la volatilité globale.

## Automatisation & Serveur (Requirements 6 & 7)
* **Hébergement** : Déploiement sur Ubuntu (AWS) avec `nohup` pour une disponibilité totale.
* **Rapport Quotidien** : Un **Cron Job** est configuré pour générer un rapport financier tous les soirs à 20h.
* **Configuration Cron** :
  `0 20 * * * /home/ubuntu/Finance_git/venv/bin/python /home/ubuntu/Finance_git/scripts/daily_report.py`
* **Stockage** : Les rapports sont sauvegardés localement sur le serveur dans le dossier `/data`.

## Structure du Projet
* `app.py` : Application principale Streamlit.
* `scripts/daily_report.py` : Script d'automatisation des rapports.
* `src/` : Modules de calculs quantitatifs.
* `data/` : Dossier de stockage des rapports générés.

##  Installation en local
1. Cloner le dépôt : `git clone https://github.com/sachalegout/Finance_git.git`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer l'app : `streamlit run app.py`
