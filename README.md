# Eurocorporate IS

Création de l'environnement Python 3.6
```bash
conda create -n py36 python=3.6
```
Activation de l'environnement
```bash
conda activate py36
```
Création d'un environnement imbriqué
```bash
python -m venv venv
```
Activation de l'environnement imbriqué
```bash
venv\Scripts\activate.bat
```
Installation des librairies
```bash
pip install -r requirements.txt
```

Pour lancer l'application : 
```bash
fbs run
```

Pour freezer l'application :
```bash
fbs freeze
``` 

Pour créer un fichier d'installation de l'application : (Nécessite de freezer auparavant)
```bash
fbs installer
```