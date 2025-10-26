# Migrate from SQLite to PostgreSQL with Docker Compose Support

## Issue Metadata
- **Labels:** `type:task`, `area:infra`, `area:kb`, `priority:P0`
- **Milestone:** M1: Requirements & Design
- **Effort:** L (3-5 days)
- **Sprint:** Sprint 1 (Nov 2025)
- **Dependencies:** None (blocking for production deployment)

## Summary

Migrate the ConfRadar database backend from SQLite to PostgreSQL to support multi-user concurrent access, better production reliability, and enable cloud deployment. Include Docker Compose orchestration for local development and testing.

## Background

Currently, the project uses SQLite as the default database (see `confradar/settings.py`). While SQLite is suitable for development and prototyping, PostgreSQL is required for:

- **Concurrent writes:** SQLite limits concurrent write operations
- **Production deployments:** Multi-container and cloud environments
- **Data integrity:** Better transaction handling and constraints
- **JSON support:** Native JSONB for future schema extensions
- **Scalability:** Better performance with larger datasets

The PRD (docs/confradar_prd.md) explicitly recommends PostgreSQL for production scenarios.

## Scope

### 1. Docker Compose Configuration
- [ ] Add PostgreSQL service to `docker-compose.yml`
  - Use official `postgres:16-alpine` image
  - Configure persistent volume for data
  - Set environment variables (user, password, database name)
  - Add health check for service readiness
- [ ] Add `pgAdmin` service (optional, for local DB management)
- [ ] Update `dagster-daemon` and `dagster-webserver` services
  - Add dependency on PostgreSQL service
  - Update `DATABASE_URL` environment variable default
  - Add connection retry logic with `depends_on` conditions

### 2. Application Configuration
- [ ] Update `packages/confradar/src/confradar/settings.py`
  - Change default `database_url` from SQLite to PostgreSQL
  - Add PostgreSQL-specific connection parameters (pool size, timeout)
  - Support both SQLite (dev/test) and PostgreSQL (prod) via env var
- [ ] Update `alembic.ini` and `alembic/env.py`
  - Ensure migrations work with PostgreSQL dialect
  - Test `compare_type` and `compare_server_default` work correctly
- [ ] Update Dagster instance configuration (`packages/confradar/dagster.yaml`)
  - Migrate from SQLite storage to PostgreSQL storage
  - Configure connection pooling for Dagster metadata

### 3. Dependencies
- [ ] Add PostgreSQL driver to `packages/confradar/pyproject.toml`
  - Add `psycopg[binary]>=3.1` (or `psycopg2-binary>=2.9`) to dependencies
  - Consider async support: `asyncpg>=0.29` if using async SQLAlchemy

### 4. Database Schema Validation
- [ ] Review existing Alembic migrations (`alembic/versions/6734aa7c5266_init_schema.py`)
  - Ensure SQLAlchemy types are PostgreSQL-compatible
  - Test timestamp handling (`DateTime(timezone=True)`)
  - Validate indexes and constraints
- [ ] Create new migration if schema adjustments needed for PostgreSQL

### 5. Testing Updates
- [ ] Update `packages/confradar/tests/test_db_models.py`
  - Keep SQLite for unit tests (fast, ephemeral)
  - Add optional PostgreSQL integration test mode (via env var)
  - Use `testcontainers-python` or Docker for integration tests
- [ ] Add test fixtures for both database backends
- [ ] Ensure tests pass with both SQLite and PostgreSQL

### 6. Documentation Updates
- [ ] Update `README.md`
  - Change Quick Start to use PostgreSQL via Docker Compose
  - Document environment variables (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`)
  - Update Alembic migration examples with PostgreSQL URL
  - Add troubleshooting section (connection issues, port conflicts)
- [ ] Update `docs/wiki/Architecture.md`
  - Replace references to "SQLite" with "PostgreSQL (SQLite for tests)"
  - Update architecture diagram to show PostgreSQL container
  - Add connection pooling and performance notes
- [ ] Update `docs/wiki/Getting-Started.md`
  - Add PostgreSQL setup instructions
  - Document how to run migrations on first setup
  - Add instructions for resetting the database
- [ ] Update `docs/wiki/Development-Guide.md`
  - Explain how to use SQLite for local dev (if needed)
  - Document PostgreSQL connection string format
  - Add database backup/restore guidance
- [ ] Update `docs/confradar_prd.md`
  - Update database section to reflect PostgreSQL as default

### 7. Environment Setup
- [ ] Create `.env.example` file with PostgreSQL defaults
  ```env
  DATABASE_URL=postgresql+psycopg://confradar:confradar@localhost:5432/confradar
  POSTGRES_USER=confradar
  POSTGRES_PASSWORD=confradar
  POSTGRES_DB=confradar
  ```
- [ ] Add `.env` to `.gitignore` (if not already present)
- [ ] Document how to override for local development

### 8. CI/CD Considerations
- [ ] Update GitHub Actions workflows (if any exist)
  - Use PostgreSQL service container in test jobs
  - Set `DATABASE_URL` to PostgreSQL in CI environment
- [ ] Add database initialization script for CI

## Implementation Plan

### Phase 1: Docker Setup (Day 1)
1. Add PostgreSQL service to `docker-compose.yml`
2. Add volumes and environment configuration
3. Test local PostgreSQL startup
4. Verify connectivity from application containers

### Phase 2: Application Changes (Day 2)
1. Add `psycopg` dependency to `pyproject.toml`
2. Update default settings in `settings.py`
3. Update Alembic configuration
4. Test migrations against PostgreSQL locally

### Phase 3: Dagster Migration (Day 3)
1. Update `dagster.yaml` to use PostgreSQL storage
2. Test Dagster daemon and webserver with PostgreSQL
3. Verify asset materializations persist correctly
4. Test run logs and event storage

### Phase 4: Testing (Day 4)
1. Update unit tests to support both backends
2. Add integration tests with PostgreSQL
3. Run full test suite against PostgreSQL
4. Fix any compatibility issues

### Phase 5: Documentation (Day 5)
1. Update all documentation files
2. Create migration guide for existing users
3. Add troubleshooting section
4. Update example commands and scripts

## Success Criteria
- [ ] PostgreSQL service starts successfully via Docker Compose
- [ ] Application connects to PostgreSQL without errors
- [ ] All Alembic migrations run successfully on PostgreSQL
- [ ] Dagster stores metadata in PostgreSQL correctly
- [ ] All tests pass with PostgreSQL backend
- [ ] Documentation is complete and accurate
- [ ] No hardcoded SQLite references remain in production code paths
- [ ] Local development workflow is documented and tested

## Non-Goals
- Migration of existing SQLite data (fresh start is acceptable for MVP)
- Database clustering or replication (future work)
- Advanced PostgreSQL features (full-text search, partitioning)
- Multi-database support in same deployment

## Risks & Mitigation
- **Risk:** Breaking existing development workflows
  - *Mitigation:* Keep SQLite as fallback for quick local testing
- **Risk:** Connection pool issues under load
  - *Mitigation:* Document recommended pool settings; add monitoring
- **Risk:** Migration incompatibilities
  - *Mitigation:* Test migrations on fresh PostgreSQL database; review generated SQL

## References
- PRD section on database: `docs/confradar_prd.md` (line 139)
- Current architecture: `docs/wiki/Architecture.md`
- SQLAlchemy PostgreSQL docs: https://docs.sqlalchemy.org/en/20/dialects/postgresql.html
- Alembic best practices: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- Docker Compose networking: https://docs.docker.com/compose/networking/

## Acceptance Checklist
- [ ] Run `docker compose up -d` and all services start healthy
- [ ] Run `uv run alembic upgrade head` and migrations complete successfully
- [ ] Run `uv run pytest` and all tests pass
- [ ] Access Dagster UI at http://localhost:3000 and verify runs are stored
- [ ] Create a conference record and verify it persists after container restart
- [ ] Documentation in README.md reflects new setup process
- [ ] At least one team member can follow docs and set up from scratch

## Estimated Effort
**L (3-5 days)** - This is a foundational change affecting multiple subsystems but with clear scope and no ambiguous requirements.

## Follow-up Issues
- Database backup/restore automation (M5)
- PostgreSQL performance tuning and indexing (M6)
- Cloud-hosted PostgreSQL setup (RDS/Cloud SQL) (M7)
- Database migration strategy for future schema changes (M4)
