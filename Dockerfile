FROM python:3.13-slim

# Setze das Arbeitsverzeichnis auf /app
WORKDIR /app

# Installiere Python-Abhängigkeiten
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den ganzen Anwendungs-Code ins Arbeitsverzeichnis
COPY . /app

# Exponiere Port 5000 (Flask)
EXPOSE 5000

# Starte die Anwendung
CMD ["python", "app.py"]