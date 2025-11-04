#!/bin/bash
set -e

echo "🚀 Setting up ConfRadar development environment in Codespaces..."

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_step() {
    echo -e "${BLUE}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Install uv if not present
print_step "Checking for uv package manager..."
if ! command -v uv &> /dev/null; then
    print_step "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    print_success "uv installed"
else
    print_success "uv already installed"
fi

# Set up Python environment
print_step "Setting up Python environment with uv..."
if [ ! -d "/workspace/packages/confradar/.venv" ]; then
    uv venv --project /workspace/packages/confradar
fi
uv sync --project /workspace/packages/confradar
print_success "Python environment ready"

# Install frontend dependencies
print_step "Installing frontend dependencies..."
if [ ! -d "/workspace/web/node_modules" ] || [ -z "$(ls -A /workspace/web/node_modules 2>/dev/null)" ]; then
    npm ci --prefix /workspace/web || npm install --prefix /workspace/web
    print_success "Frontend dependencies installed"
else
    print_success "Frontend dependencies already installed"
fi

# Wait for Docker services to be ready
print_step "Starting Docker services..."
docker compose --project-directory /workspace up -d

print_step "Waiting for PostgreSQL to be ready..."
timeout=60
elapsed=0
until docker compose --project-directory /workspace exec -T postgres pg_isready -U confradar > /dev/null 2>&1; do
    if [ $elapsed -ge $timeout ]; then
        print_warning "PostgreSQL did not start within ${timeout}s. You may need to restart services manually."
        break
    fi
    echo -n "."
    sleep 2
    elapsed=$((elapsed + 2))
done

if [ $elapsed -lt $timeout ]; then
    print_success "PostgreSQL is ready"
    
    # Run database migrations
    print_step "Running database migrations..."
    uv run --project /workspace/packages/confradar alembic upgrade head
    print_success "Database migrations completed"
else
    print_warning "Skipping database migrations due to PostgreSQL timeout"
fi

# Wait for Dagster to be ready
print_step "Waiting for Dagster web UI to be ready..."
timeout=30
elapsed=0
until curl -sf http://localhost:3000/server_info > /dev/null 2>&1; do
    if [ $elapsed -ge $timeout ]; then
        print_warning "Dagster web UI did not start within ${timeout}s. It may still be starting up."
        break
    fi
    echo -n "."
    sleep 2
    elapsed=$((elapsed + 2))
done

if [ $elapsed -lt $timeout ]; then
    print_success "Dagster web UI is ready"
fi

# Display success message with URLs
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ ConfRadar Development Environment Ready!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Available Services:${NC}"
echo -e "  • Dagster UI:      ${YELLOW}http://localhost:3000${NC}"
echo -e "  • Frontend Dev:    ${YELLOW}http://localhost:3100${NC} (use 'npm run dev' in web/)"
echo -e "  • pgAdmin:         ${YELLOW}http://localhost:5050${NC}"
echo -e "  • LiteLLM Proxy:   ${YELLOW}http://localhost:4000${NC}"
echo -e "  • PostgreSQL:      ${YELLOW}localhost:5432${NC}"
echo ""
echo -e "${BLUE}Quick Start Commands:${NC}"
echo -e "  • Run tests:       ${YELLOW}cd packages/confradar && uv run pytest${NC}"
echo -e "  • Frontend dev:    ${YELLOW}cd web && npm run dev${NC}"
echo -e "  • Dagster CLI:     ${YELLOW}cd packages/confradar && uv run dagster dev${NC}"
echo ""
echo -e "${BLUE}Environment Variables:${NC}"
if [ -n "$OPENAI_API_KEY" ] || [ -n "$CONFRADAR_SA_OPENAI" ]; then
    echo -e "  ${GREEN}✓${NC} API keys configured"
else
    echo -e "  ${YELLOW}⚠${NC} Set OPENAI_API_KEY or CONFRADAR_SA_OPENAI in Codespace secrets"
fi
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo -e "  • Setup Guide:     ${YELLOW}docs/CODESPACES_SETUP.md${NC}"
echo -e "  • Wiki:            ${YELLOW}wiki/Development-Guide.md${NC}"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"
