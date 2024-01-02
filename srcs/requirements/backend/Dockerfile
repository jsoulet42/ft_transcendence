# Utiliser une image Python Alpine
FROM python:3.8-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Installer les dépendances nécessaires pour PostgreSQL
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Copier le fichier des dépendances et installer les packages
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copier le reste des fichiers de l'application dans le conteneur
COPY . /home/groot/data/backend/api

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
