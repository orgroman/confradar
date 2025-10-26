# PostgreSQL Migration - Implementation Checklist

Use this checklist when implementing the PostgreSQL migration. Check off items as you complete them.

## Pre-Implementation

- [ ] Review the [full issue document](issues/postgres-migration.md)
- [ ] Review the [migration summary](POSTGRES_MIGRATION_SUMMARY.md)
- [ ] Create a new branch: `git checkout -b feature/postgres-migration`
- [ ] Backup any existing local SQLite databases (if needed)

## Phase 1: Docker Compose Setup

### PostgreSQL Service
- [ ] Add PostgreSQL service to `docker-compose.yml`
  - [ ] Use `postgres:16-alpine` image
  - [ ] Configure environment variables (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`)
  - [ ] Add persistent volume (`postgres_data`)
  - [ ] Add health check
  - [ ] Expose port 5432
- [ ] Add pgAdmin service (optional)
  - [ ] Use `dpage/pgadmin4` image
  - [ ] Configure default admin email and password
  - [ ] Expose port 5050
- [ ] Update `dagster-daemon` service
  - [ ] Add `depends_on` with PostgreSQL health check
  - [ ] Update `DATABASE_URL` default to PostgreSQL
- [ ] Update `dagster-webserver` service
  - [ ] Add `depends_on` with PostgreSQL health check
  - [ ] Update `DATABASE_URL` default to PostgreSQL
- [ ] Add `postgres_data` volume to volumes section

### Testing
- [ ] Run `docker compose up -d postgres`
- [ ] Verify PostgreSQL starts: `docker compose ps`
- [ ] Check logs: `docker compose logs postgres`
- [ ] Test connection: `docker compose exec postgres psql -U confradar -d confradar -c '\dt'`

## Phase 2: Dependencies

- [ ] Add `psycopg[binary]>=3.1` to `packages/confradar/pyproject.toml` dependencies
  - Alternative: `psycopg2-binary>=2.9`
- [ ] Run `uv sync` to install new dependencies
- [ ] Verify import works: `uv run python -c "import psycopg"`

## Phase 3: Application Configuration

### Settings
- [ ] Update `packages/confradar/src/confradar/settings.py`
  - [ ] Change default `database_url` to PostgreSQL connection string
  - [ ] Add comment about SQLite override for testing
- [ ] Create `.env.example` with PostgreSQL defaults
  ```env
  DATABASE_URL=postgresql+psycopg://confradar:confradar@localhost:5432/confradar
  POSTGRES_USER=confradar
  POSTGRES_PASSWORD=confradar
  POSTGRES_DB=confradar
  ```
- [ ] Verify `.env` is in `.gitignore`

### Alembic
- [ ] Review `alembic/env.py` (should work as-is)
- [ ] Test migration generation: `uv run alembic revision --autogenerate -m "test postgres"`
  - [ ] Delete test migration if successful
- [ ] Run migrations: `uv run alembic upgrade head`
- [ ] Verify tables created: `docker compose exec postgres psql -U confradar -d confradar -c '\dt'`

## Phase 4: Dagster Configuration

- [ ] Update `packages/confradar/dagster.yaml`
  - [ ] Change `storage.sqlite` to `storage.postgres`
  - [ ] Add PostgreSQL connection configuration
- [ ] Restart Dagster services: `docker compose restart dagster-daemon dagster-webserver`
- [ ] Access Dagster UI: http://localhost:3000
- [ ] Verify runs are stored in PostgreSQL
- [ ] Materialize a test asset and verify it persists

## Phase 5: Testing

### Unit Tests
- [ ] Review `packages/confradar/tests/test_db_models.py`
- [ ] Ensure tests still use SQLite (fast ephemeral databases)
- [ ] Run unit tests: `cd packages/confradar; uv run pytest tests/test_db_models.py -v`
- [ ] Verify all tests pass

### Integration Tests (Optional)
- [ ] Add PostgreSQL integration test mode
  - [ ] Check for `TEST_DATABASE_URL` environment variable
  - [ ] Use Docker test containers or test database
- [ ] Run integration tests against PostgreSQL
- [ ] Verify all tests pass

### Full Test Suite
- [ ] Run complete test suite: `uv run pytest -v`
- [ ] Verify code coverage: `uv run pytest --cov=confradar`
- [ ] Fix any failing tests

### Manual Testing
- [ ] Start all services: `docker compose up -d`
- [ ] Create a test conference record via Python:
  ```python
  from confradar.db.models import Conference
  from confradar.db.base import get_engine
  from sqlalchemy.orm import Session
  
  engine = get_engine()
  with Session(engine) as session:
      conf = Conference(
          title="Test Conference 2025",
          key="test_2025",
          year=2025
      )
      session.add(conf)
      session.commit()
      print(f"Created conference ID: {conf.id}")
  ```
- [ ] Verify record persists after container restart
- [ ] Query via psql: `docker compose exec postgres psql -U confradar -d confradar -c 'SELECT * FROM conference;'`

## Phase 6: Documentation

### Core Documentation
- [x] Update `ROADMAP.md` - Add PostgreSQL migration to M1
- [x] Update `docs/wiki/Architecture.md` - Update Data Storage Layer section
- [x] Update `docs/wiki/Overview.md` - Update Technology Stack section
- [ ] Update `README.md` - Update Quick Start with PostgreSQL setup
  - [ ] Add Docker Compose startup instructions
  - [ ] Update database migration examples
  - [ ] Add troubleshooting section
- [ ] Update `docs/wiki/Getting-Started.md`
  - [ ] Add PostgreSQL prerequisites
  - [ ] Document environment variables
  - [ ] Add first-time setup instructions
- [ ] Update `docs/wiki/Development-Guide.md`
  - [ ] Document PostgreSQL connection strings
  - [ ] Add backup/restore guide
  - [ ] Add troubleshooting tips

### Additional Documentation
- [x] Create `docs/issues/postgres-migration.md` (full issue)
- [x] Create `docs/POSTGRES_MIGRATION_SUMMARY.md` (summary)
- [x] Create `docs/POSTGRES_MIGRATION_CHECKLIST.md` (this file)
- [ ] Update `docs/confradar_prd.md` database section (if needed)

## Phase 7: Validation & Cleanup

### Final Validation
- [ ] Fresh clone test: Clone repo in new directory and follow setup docs
- [ ] Verify Docker Compose brings up all services successfully
- [ ] Run migrations from scratch: `uv run alembic upgrade head`
- [ ] Run full test suite: `uv run pytest`
- [ ] Access Dagster UI and materialize assets
- [ ] Verify data persists across restarts

### Code Cleanup
- [ ] Remove any SQLite-specific code (if any)
- [ ] Update code comments referencing SQLite
- [ ] Remove hardcoded SQLite paths
- [ ] Search for remaining SQLite references: `grep -r "sqlite" --exclude-dir=.git --exclude-dir=__pycache__`
  - Keep: Test files, .gitignore entries
  - Remove: Production code, primary documentation

### Git
- [ ] Review all changes: `git status`
- [ ] Commit configuration files: `git add docker-compose.yml .env.example pyproject.toml`
- [ ] Commit application changes: `git add packages/confradar/src/confradar/`
- [ ] Commit Dagster config: `git add packages/confradar/dagster.yaml`
- [ ] Commit documentation: `git add docs/ README.md ROADMAP.md`
- [ ] Write comprehensive commit message
- [ ] Push branch: `git push origin feature/postgres-migration`

## Phase 8: Review & Merge

- [ ] Create Pull Request on GitHub
- [ ] Reference issue: "Closes #XX" (insert issue number)
- [ ] Add labels: `type:task`, `area:infra`, `area:kb`, `priority:P0`
- [ ] Request review (or self-review if solo)
- [ ] Ensure CI passes (if configured)
- [ ] Address review comments
- [ ] Merge to main branch
- [ ] Delete feature branch
- [ ] Close issue

## Post-Migration

- [ ] Update team/collaborators about new setup process
- [ ] Monitor for issues in production
- [ ] Document any lessons learned
- [ ] Plan follow-up work:
  - [ ] Database backup automation
  - [ ] Performance tuning and indexing
  - [ ] Cloud deployment (RDS/Cloud SQL)
  - [ ] Monitoring and alerting

## Rollback (If Needed)

If critical issues arise:
- [ ] Revert docker-compose.yml changes
- [ ] Set `DATABASE_URL=sqlite:///confradar.db` in environment
- [ ] Restart services
- [ ] Document issues encountered
- [ ] Plan fixes before re-attempting

## Success Criteria

All of these must be true before marking complete:

- [x] Issue document created and tracked
- [ ] PostgreSQL service runs in Docker Compose
- [ ] Application connects to PostgreSQL without errors
- [ ] All Alembic migrations succeed
- [ ] Dagster stores metadata in PostgreSQL
- [ ] All tests pass
- [ ] Documentation is complete and accurate
- [ ] Fresh setup works from docs alone
- [ ] No SQLite references in production code
- [ ] Changes reviewed and merged

---

**Estimated Time**: 3-5 days  
**Priority**: P0  
**Milestone**: M1

**Start Date**: ___________  
**Completion Date**: ___________

**Notes**: 
```
(Add any implementation notes, blockers, or decisions here)
```
