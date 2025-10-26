# Data Schema

This page summarizes the core database entities used by ConfRadar. For full details, see the SQLAlchemy models and Alembic migrations in the repository.

- Models: `packages/confradar/src/confradar/db/models.py`
- Base/engine: `packages/confradar/src/confradar/db/base.py`
- Migrations: `alembic/versions/`

## Entities

- Conference
  - id (PK)
  - source (site/spider)
  - name, acronym
  - year, location, url
  - submission_deadline, notification_date, camera_ready_date, conference_start, conference_end
  - metadata_json (raw scraped/extracted fields)
  - created_at, updated_at

- RawDocument
  - id (PK)
  - source_url, fetched_at
  - content (HTML/text)
  - hash

- Extraction
  - id (PK)
  - document_id (FK RawDocument)
  - model/provider
  - fields_json (structured extraction)
  - confidence

Note: Exact names and relationships are defined in the code and may evolve. Run Alembic migrations to update your schema.

## Migrations (Alembic)

```powershell
uv run alembic upgrade head
```

To create a new migration:

```powershell
uv run alembic revision --autogenerate -m "add constraints"
```
