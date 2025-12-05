# Utilisation d'une image Python légère
FROM python:3.12-slim

# Définition du dossier de travail dans le conteneur
WORKDIR /app

# Copie des dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY app.py .
# On copie aussi le fichier blacklist s'il existe déjà
COPY blocked_keys.json* .

# Exposition du port Flask
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]