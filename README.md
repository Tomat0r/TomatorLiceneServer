# License Management API

Diese Anwendung ist eine einfache Lizenzverwaltungs-API, die mit Flask erstellt wurde. Sie ermöglicht die Generierung, das Auflisten und das Löschen von Lizenzschlüsseln. 

## Funktionen

- **Generieren**: Erstellt einen neuen, eindeutigen Lizenzschlüssel.
- **Auflisten**: Zeigt alle gespeicherten Lizenzschlüssel an.
- **Löschen**: Entfernt einen Lizenzschlüssel aus der Datenbank.

---

## Voraussetzungen

- **Python 3.13+**
- **Docker** und **docker-compose** (für die Containerisierung)

---

## Installation & Nutzung

### 1. Anwendung ohne Docker ausführen

1. **Clone das Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Installiere die Abhängigkeiten**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setze die Umgebungsvariable**:
   ```bash
   export ADMIN_PASSWORD=<dein_admin_passwort>
   ```

4. **Starte die Anwendung**:
   ```bash
   python app.py
   ```

Die API läuft standardmäßig auf `http://localhost:5000`.

---

### 2. Anwendung mit Docker ausführen

1. **Baue und starte die Container**:
   ```bash
   docker-compose up --build
   ```

2. **Setze die Umgebungsvariable in der `.env`-Datei**:
   Erstelle eine `.env`-Datei im Projektverzeichnis:
   ```plaintext
   ADMIN_PASSWORD=<dein_admin_passwort>
   ```

Die API läuft anschließend unter `http://localhost:5000`.

---

## API-Endpunkte

### 1. **POST** `/generate`
Generiert einen neuen Lizenzschlüssel.  
**Body**:
```json
{
  "password": "<Admin-Passwort>"
}
```

**Response** (Erfolg):
```json
{
  "success": true,
  "key": "XXXXX-XXXXX-XXXXX-XXXXX"
}
```

---

### 2. **GET** `/list`
Listet alle vorhandenen Lizenzen.  
**Query-Parameter**:  
`password=<Admin-Passwort>`

**Response** (Erfolg):
```json
[
  {
    "key": "XXXXX-XXXXX-XXXXX-XXXXX",
    "uuid": null,
    "creation_date": "2023-10-28T12:00:00"
  }
]
```

---

### 3. **DELETE** `/delete`
Löscht eine Lizenz aus der Datenbank.  
**Body**:
```json
{
  "password": "<Admin-Passwort>",
  "key": "XXXXX-XXXXX-XXXXX-XXXXX"
}
```

**Response** (Erfolg):
```json
{
  "success": true
}
```

---

## Hinweise

- Das Admin-Passwort **muss** als Umgebungsvariable gesetzt werden, entweder direkt in der Umgebung oder über die `.env`-Datei bei Verwendung von Docker.
- Die Lizenzdatenbank ist eine SQLite-Datenbank und wird automatisch im Arbeitsverzeichnis unter `licenses.db` erstellt.

---

## Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**. Siehe die `LICENSE`-Datei für weitere Informationen.
