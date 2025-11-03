# pgAdmin Configuration

This directory contains configuration files for pgAdmin to automatically set up the Confradar PostgreSQL database server.

## Files

### `servers.json`
Defines the PostgreSQL server connection details. pgAdmin will automatically load this configuration on startup:
- **Name**: Confradar Postgres
- **Host**: `postgres` (Docker service name)
- **Port**: `5432`
- **Database**: `confradar`
- **Username**: `confradar`

### `pgpass` (optional, not used)
pgAdmin doesn't support pgpass files in the standard way. Password must be entered manually on first connection or saved via pgAdmin's interface.

## Usage

### First Time Setup

1. **Start services:**
   ```bash
   docker compose up postgres pgadmin
   ```

2. **Access pgAdmin:**
   - Open http://localhost:5050 in your browser
   - Login with:
     - **Email**: `admin@example.com` (or from `.env`)
     - **Password**: `admin` (or from `.env`)

3. **Connect to Postgres:**
   - The "Confradar Postgres" server will appear in the left sidebar
   - Click on it to connect
   - Enter password: `confradar` (or from `.env`)
   - ✅ Check "Save Password" to avoid entering it again

### Subsequent Access

After the first connection with "Save Password" checked, pgAdmin will automatically connect to the database on future visits.

## Environment Variables

You can customize the configuration using environment variables in your `.env` file:

```env
# pgAdmin login credentials
PGADMIN_DEFAULT_EMAIL=your-email@example.com
PGADMIN_DEFAULT_PASSWORD=your-secure-password

# PostgreSQL credentials (must match postgres service)
POSTGRES_USER=confradar
POSTGRES_PASSWORD=confradar
POSTGRES_DB=confradar
```

## Security Note

- pgAdmin stores saved passwords encrypted in its internal database (`/var/lib/pgadmin/pgadmin4.db`)
- For production, use strong passwords and consider using pgAdmin in server mode with proper authentication
- The current configuration uses desktop mode (`SERVER_MODE: False`) suitable for local development
