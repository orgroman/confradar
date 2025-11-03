# GitHub Codespaces Setup Guide

Get started with ConfRadar development in seconds using GitHub Codespaces—no local setup required!

## Quick Start

### 1. Launch Codespace

Click the button below or use the GitHub UI:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/orgroman/confradar?quickstart=1)

**Or manually:**
1. Go to the [ConfRadar repository](https://github.com/orgroman/confradar)
2. Click the green **Code** button
3. Select the **Codespaces** tab
4. Click **Create codespace on main**

### 2. Wait for Setup

The Codespace will automatically:
- ✅ Install Python 3.12 and uv package manager
- ✅ Install Node.js 20 for frontend development
- ✅ Set up Docker-in-Docker for services
- ✅ Install all Python dependencies (`uv sync`)
- ✅ Install all frontend dependencies (`npm install`)
- ✅ Start PostgreSQL, Dagster, LiteLLM, and pgAdmin
- ✅ Run database migrations

**Expected setup time:** 3-5 minutes

### 3. Configure API Keys (Required)

You need to configure OpenAI API access before running scrapers or LLM features.

**Option A: Add Codespace Secret (Recommended)**
1. Go to your [GitHub Settings → Codespaces](https://github.com/settings/codespaces)
2. Click **New secret**
3. Add one of:
   - `CONFRADAR_SA_OPENAI` (for organization service account key)
   - `OPENAI_API_KEY` (for personal API key: `sk-...`)
4. Select repository: `orgroman/confradar`
5. Restart your Codespace to apply

**Option B: Set in Terminal**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
# Or
export CONFRADAR_SA_OPENAI="your-service-account-key"
```

### 4. Access Services

Once setup completes, access these services via forwarded ports:

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| **Dagster UI** | 3000 | http://localhost:3000 | Pipeline orchestration and monitoring |
| **Frontend Dev** | 3100 | http://localhost:3100 | Next.js development server |
| **pgAdmin** | 5050 | http://localhost:5050 | Database management UI |
| **LiteLLM** | 4000 | http://localhost:4000 | LLM proxy service |
| **PostgreSQL** | 5432 | localhost:5432 | Database server |

**Port forwarding is automatic!** GitHub will notify you when ports are forwarded.

## Development Workflow

### Running Tests
```bash
cd packages/confradar
uv run pytest                    # Run all tests
uv run pytest tests/test_db.py   # Run specific test file
uv run pytest -v                 # Verbose output
```

### Frontend Development
```bash
cd web
npm run dev        # Start Next.js dev server on port 3100
npm run build      # Production build
npm run lint       # Lint code
npm test           # Run tests
```

### Backend Development
```bash
cd packages/confradar

# Run scrapers
uv run scrapy crawl ai_deadlines

# Dagster CLI
uv run dagster dev               # Start Dagster locally (alternative to Docker)
uv run dagster asset materialize --select store_conferences

# Database migrations
uv run alembic upgrade head      # Apply migrations
uv run alembic revision --autogenerate -m "description"  # Create migration
```

### Docker Services Management
```bash
# View service status
docker compose ps

# View logs
docker compose logs -f            # All services
docker compose logs -f dagster-webserver  # Specific service

# Restart services
docker compose restart dagster-webserver
docker compose restart postgres

# Stop all services
docker compose down

# Start services again
docker compose up -d
```

## Codespace Configuration

### Installed VS Code Extensions

The Codespace comes pre-configured with:
- **Python**: Python extension, Pylance, debugpy
- **Linting/Formatting**: Ruff (Python), ESLint (TypeScript), Prettier
- **Docker**: Docker extension for managing containers
- **Database**: SQLTools with PostgreSQL driver
- **AI**: GitHub Copilot (if enabled for your account)
- **Frontend**: Tailwind CSS IntelliSense
- **Git**: GitLens for enhanced Git features

### Python Configuration

- **Interpreter**: Auto-configured to use `/workspace/.venv/bin/python`
- **Formatter**: Ruff (format on save enabled)
- **Linter**: Ruff
- **Import organization**: Automatic on save

### Environment Variables

Environment variables are configured in `.devcontainer/devcontainer.json`:

```json
"remoteEnv": {
  "DATABASE_URL": "postgresql+psycopg2://confradar:confradar@postgres:5432/confradar",
  "DAGSTER_HOME": "/workspace/packages/confradar/dagster_home",
  "CONFRADAR_SA_OPENAI": "${localEnv:CONFRADAR_SA_OPENAI}",
  "OPENAI_API_KEY": "${localEnv:OPENAI_API_KEY}"
}
```

## Troubleshooting

### Services Not Starting

**Check Docker status:**
```bash
docker compose ps
docker compose logs
```

**Restart all services:**
```bash
docker compose down
docker compose up -d
```

### Python Environment Issues

**Recreate virtual environment:**
```bash
cd packages/confradar
rm -rf .venv
uv venv
uv sync
```

### Database Connection Issues

**Check PostgreSQL is running:**
```bash
docker compose ps postgres
docker exec confradar-postgres pg_isready -U confradar
```

**Reset database:**
```bash
docker compose down -v  # WARNING: This deletes all data!
docker compose up -d postgres
uv run alembic upgrade head
```

### Frontend Build Issues

**Clear Next.js cache:**
```bash
cd web
rm -rf .next node_modules
npm ci
npm run dev
```

### Port Already in Use

If ports are conflicted:
1. Check forwarded ports in VS Code "Ports" tab
2. Stop conflicting services: `docker compose down`
3. Change port in `docker-compose.yml` if needed

### Out of Memory

Codespaces may have memory limits. To reduce usage:
```bash
# Stop unused services
docker compose stop web  # If not doing frontend work
docker compose stop pgadmin  # If not using pgAdmin
```

### Slow Performance

**Enable file watching optimization:**
```bash
export CHOKIDAR_USEPOLLING=true
export WATCHPACK_POLLING=true
```

## Tips & Best Practices

### 1. Use the Integrated Terminal
VS Code's terminal is pre-configured with the correct environment. Use it for all commands.

### 2. Commit Often
Codespaces are ephemeral. Commit and push your work frequently!

### 3. Use Port Forwarding
All ports are automatically forwarded. Click "Open in Browser" from the Ports tab.

### 4. Stop When Not Using
Codespaces auto-stop after 30 minutes of inactivity. You can also manually stop them to save resources.

### 5. Prebuild Configuration (Future)
For faster startup, we can configure prebuilds. See [GitHub Docs](https://docs.github.com/en/codespaces/prebuilding-your-codespaces).

## Resource Limits

GitHub provides free Codespaces usage:
- **Free plan**: 120 core-hours/month (60 hours on 2-core machine)
- **Pro plan**: 180 core-hours/month

**To check usage:**
1. Go to [GitHub Settings → Billing → Codespaces](https://github.com/settings/billing)
2. View your usage and limits

## Local Development Alternative

Prefer working locally? See our [Development Guide](../wiki/Development-Guide.md) for local setup instructions.

## Advanced Configuration

### Custom Devcontainer

You can create specialized devcontainers for focused work:

**Backend-only:**
```bash
# Create .devcontainer/backend/devcontainer.json
# Exclude frontend features (Node, npm)
```

**Frontend-only:**
```bash
# Create .devcontainer/frontend/devcontainer.json
# Exclude Python, Dagster, PostgreSQL
```

### Lifecycle Scripts

- **postCreateCommand**: Runs once after Codespace creation (setup script)
- **postStartCommand**: Runs every time Codespace starts (starts Docker services)
- **postAttachCommand**: Runs when VS Code attaches (future use)

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/orgroman/confradar/issues)
- **Wiki**: [Project Wiki](https://github.com/orgroman/confradar/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/orgroman/confradar/discussions)

## Next Steps

1. ✅ Launch your Codespace
2. ✅ Configure API keys
3. ✅ Explore services (Dagster UI, pgAdmin)
4. ✅ Run tests to verify setup
5. 🚀 Start contributing!

---

**Last Updated**: November 2025  
**Maintained By**: ConfRadar Team
