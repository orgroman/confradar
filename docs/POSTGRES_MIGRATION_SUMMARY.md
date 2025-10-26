# PostgreSQL Migration - Summary

## Decision

**Migration from SQLite to PostgreSQL as the primary database for ConfRadar.**

## Rationale

SQLite was initially used for rapid prototyping and local development, but PostgreSQL is necessary for:

1. **Production Readiness**
   - Better concurrent write handling
   - Robust transaction management
   - Cloud deployment compatibility (RDS, Cloud SQL, etc.)

2. **Scalability**
   - Connection pooling
   - Better performance with larger datasets
   - Advanced indexing capabilities

3. **Features**
   - Native JSON/JSONB support for future schema flexibility
   - Full-text search capabilities
   - Better data integrity constraints

4. **Alignment with PRD**
   - The original PRD (docs/confradar_prd.md) explicitly recommends PostgreSQL for multi-user and production scenarios

## Impact

### Components Affected

1. **Docker Compose** (`docker-compose.yml`)
   - Add PostgreSQL service with persistent volumes
   - Update Dagster services to depend on PostgreSQL
   - Optional: Add pgAdmin for database management

2. **Application Settings** (`packages/confradar/src/confradar/settings.py`)
   - Change default `database_url` from SQLite to PostgreSQL
   - Add PostgreSQL connection parameters

3. **Database Migrations** (`alembic/`)
   - Validate existing migrations work with PostgreSQL
   - Update `alembic/env.py` configuration

4. **Dagster Configuration** (`packages/confradar/dagster.yaml`)
   - Migrate Dagster metadata storage from SQLite to PostgreSQL

5. **Dependencies** (`packages/confradar/pyproject.toml`)
   - Add `psycopg[binary]` or `psycopg2-binary` for PostgreSQL driver

6. **Tests** (`packages/confradar/tests/`)
   - Keep SQLite for fast unit tests
   - Add PostgreSQL integration tests (optional)

7. **Documentation**
   - README.md - Update Quick Start and setup instructions
   - docs/wiki/Architecture.md - Update database section
   - docs/wiki/Getting-Started.md - Add PostgreSQL setup guide
   - docs/wiki/Development-Guide.md - Document connection strings and troubleshooting

### What Stays the Same

- **SQLAlchemy ORM**: No changes to model definitions or query patterns
- **Alembic migrations**: Existing migration scripts remain compatible
- **Application code**: Database abstraction means no business logic changes
- **SQLite for tests**: Unit tests can continue using in-memory SQLite for speed

## Timeline

**Priority: P0 (Blocking for production deployment)**  
**Milestone: M1 (Q4 2025)**  
**Effort: L (3-5 days)**

### Phases

1. **Day 1**: Docker Compose setup and PostgreSQL service configuration
2. **Day 2**: Application configuration and dependency updates
3. **Day 3**: Dagster storage migration and testing
4. **Day 4**: Test suite updates and validation
5. **Day 5**: Documentation updates and developer guides

## Developer Experience

### Before (SQLite)
```powershell
# Start services
docker compose up -d

# Migrations create local SQLite file
uv run alembic upgrade head
# Creates: confradar.db (local file)

# Run application
uv run confradar fetch https://example.org/cfp
```

### After (PostgreSQL)
```powershell
# Start all services (includes PostgreSQL)
docker compose up -d

# Wait for PostgreSQL to be ready (health check)
# Migrations run against PostgreSQL
uv run alembic upgrade head

# Run application (connects to PostgreSQL)
uv run confradar fetch https://example.org/cfp

# Optional: Access pgAdmin at http://localhost:5050
```

### Environment Variables
```env
# PostgreSQL connection (new default)
DATABASE_URL=postgresql+psycopg://confradar:confradar@localhost:5432/confradar

# PostgreSQL service configuration
POSTGRES_USER=confradar
POSTGRES_PASSWORD=confradar
POSTGRES_DB=confradar

# Override for local SQLite (testing only)
DATABASE_URL=sqlite:///test.db
```

## Rollback Plan

If issues arise during migration:

1. **Keep SQLite support**: The application will still support SQLite via `DATABASE_URL`
2. **Use feature flags**: Guard PostgreSQL-specific features
3. **Parallel operation**: Run both databases temporarily if needed
4. **Revert docker-compose**: Remove PostgreSQL service if blocking

## Follow-up Work

After initial migration (tracked in separate issues):

1. **Performance tuning**: Index optimization, query analysis
2. **Backup/restore**: Automated backup scripts
3. **Cloud deployment**: RDS/Cloud SQL setup (M7)
4. **Monitoring**: Database metrics and alerting (M6)
5. **Connection pooling**: PgBouncer or similar for high concurrency

## References

- **Issue**: [PostgreSQL Migration Issue](issues/postgres-migration.md)
- **PRD**: `docs/confradar_prd.md` (Database section, line 139)
- **Architecture**: `docs/wiki/Architecture.md` (Data Storage Layer)
- **Roadmap**: `ROADMAP.md` (M1 milestone)

## Questions & Answers

**Q: Why not just stick with SQLite?**  
A: SQLite has concurrency limitations and is not suitable for production deployments with multiple workers or cloud environments.

**Q: Will this break my local development setup?**  
A: No. Docker Compose will handle PostgreSQL automatically. If you prefer SQLite locally, you can still override `DATABASE_URL`.

**Q: Do we need to migrate existing data?**  
A: No. This is early in development (MVP phase), so starting fresh is acceptable.

**Q: What about existing migrations?**  
A: They will work as-is. Alembic migrations are database-agnostic when using SQLAlchemy types correctly.

**Q: Can I use a different PostgreSQL host?**  
A: Yes. Set `DATABASE_URL` to point to any PostgreSQL instance (local, Docker, cloud, etc.).

**Q: What if I don't have Docker?**  
A: You can install PostgreSQL locally and set `DATABASE_URL` to your local instance. Docker Compose is recommended but not required.

## Approval

This migration aligns with:
- ✅ Original PRD recommendations
- ✅ Production deployment requirements
- ✅ Industry best practices
- ✅ M1 milestone goals (foundation for MVP)

**Status**: Ready for implementation  
**Next Step**: Create GitHub issue and assign to Sprint 1

---

**Last Updated**: 2025-10-26  
**Document Owner**: @orgroman
