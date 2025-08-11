# Copilot Instructions for incidentes_controle_divciber

## Project Overview
- This is a Flask-based web application for managing and analyzing incident reports, using SQLAlchemy for ORM and a modular blueprint structure for features.
- The main entry point is `run.py`. Application logic is organized under the `app/` directory.

## Key Components
- `app/models.py`: Defines SQLAlchemy models. Relationships use `db.relationship` and `backref` for bidirectional access (e.g., `User` ↔ `Analise`).
- `app/blueprints/`: Contains feature modules (e.g., `analise`, `main`). Each blueprint has its own routes, templates, and static files.
- `app/__init__.py`: Initializes the Flask app and extensions (e.g., SQLAlchemy).
- `database.py`: Handles database setup and migrations.
- `requirements.txt`: Lists Python dependencies.

## Patterns & Conventions
- Models use lowercase `db.model` (should be `db.Model` for SQLAlchemy; check for consistency).
- Relationships are defined with `db.relationship` and `backref` for easy navigation between models.
- Blueprints are used for modularizing routes and templates. Each feature has its own folder under `app/blueprints/` and `app/templates/`.
- Static assets are organized under `app/static/` by type (css, js).

## Developer Workflows
- **Run the app:** `python run.py` (ensure dependencies from `requirements.txt` are installed)
- **Database migrations:** Use Flask-Migrate or manual scripts (check `database.py` for details).
- **Add a new feature:** Create a new blueprint under `app/blueprints/`, add routes, templates, and register in `app/__init__.py`.
- **Model changes:** Update `app/models.py` and apply migrations.

## Integration Points
- Uses Flask, SQLAlchemy, and Werkzeug for password hashing.
- Templates use Jinja2 (default for Flask).
- No explicit API or external service integration found in the current structure.

## Examples
- To add a new model:
  ```python
  class Example(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      # ...
  ```
- To add a new blueprint:
  - Create a folder in `app/blueprints/` and `app/templates/`.
  - Register the blueprint in `app/__init__.py`.

## Notes
- Check for typos in model base class (`db.model` vs `db.Model`).
- Keep model and blueprint structure consistent for maintainability.
- Update this file as new conventions or workflows are established.
