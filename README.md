
# Versicherungsverwaltung

Dieses Projekt ist ein webbasiertes Versicherungsverwaltungssystem, das auf Django basiert. Es ermöglicht das Verwalten von Kunden, Mitarbeitern, Schadensfällen und Versicherungsverträgen.

## Features

- Verwaltung von Kunden, Mitarbeitern, Schadensfällen und Versicherungsverträgen
- Erstellen, Anzeigen, Bearbeiten und Löschen von Kunden, Mitarbeitern, Schadensfällen und Versicherungsverträgen
- REST API für den Zugriff auf Kunden, Mitarbeiter, Schadensfälle und Versicherungsverträge
- Benutzerfreundliche Oberfläche

## Voraussetzungen

- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+

## Installation

1. Klonen Sie das Repository:

   ```
   git clone https://github.com/yourusername/versicherung_django.git
   cd versicherung_django
   ```

2. Erstellen Sie eine virtuelle Umgebung und aktivieren Sie sie:

   ```
   python -m venv venv
   source venv/bin/activate  # Für Windows: venv\Scripts\activate
   ```

3. Installieren Sie die erforderlichen Pakete:

   ```
   pip install -r requirements.txt
   ```

4. Führen Sie die Migrationen aus:

   ```
   python manage.py migrate
   ```

5. Erstellen Sie einen Superuser:

   ```
   python manage.py createsuperuser
   ```

6. Starten Sie den Entwicklungsserver:

   ```
   python manage.py runserver
   ```

7. Öffnen Sie einen Webbrowser und navigieren Sie zu `http://127.0.0.1:8000/`.

## Verwendung

Navigieren Sie zu den verschiedenen Abschnitten des Projekts, um Kunden, Mitarbeiter, Schadensfälle und Versicherungsverträge zu verwalten:

- Kunden: `http://127.0.0.1:8000/orga/kunden/`
- Mitarbeiter: `http://127.0.0.1:8000/orga/mitarbeiter/`
- Schadensfälle: `http://127.0.0.1:8000/orga/schadensfall/`
- Versicherungsverträge: `http://127.0.0.1:8000/orga/versicherungsvertrag/`

Um die REST-API zu verwenden, verwenden Sie die folgenden Endpunkte:

- Kunden: `http://127.0.0.1:8000/orga/api/kunden/`
- Mitarbeiter: `http://127.0.0.1:8000/orga/api/mitarbeiter/`
- Schadensfälle: `http://127.0.0.1:8000/orga/api/schaeden/`
- Versicherungsverträge: `http://127.0.0.1:8000/orga/api/vertraege/`

## Mitwirkende

- dennisjanvogt (GitHub-Username)


## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe die [LICENSE](LICENSE) Datei für weitere Informationen.

