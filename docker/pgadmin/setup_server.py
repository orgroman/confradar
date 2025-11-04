#!/usr/bin/env python3
"""
Pre-configure pgAdmin with server connection and saved password.
This script runs on container startup to set up the default server.
"""

import os
import sqlite3
from pathlib import Path

# Configuration
PGADMIN_DB = "/var/lib/pgadmin/pgadmin4.db"
SERVER_CONFIG = {
    "name": "Confradar Postgres",
    "group": 1,  # Servers group
    "host": "postgres",
    "port": 5432,
    "maintenance_db": "confradar",
    "username": "confradar",
    "password": os.getenv("POSTGRES_PASSWORD", "confradar"),
    "ssl_mode": "prefer",
    "connect_now": True,
}


def setup_server():
    """Add server configuration with saved password to pgAdmin database."""
    
    # Wait for pgAdmin database to be created
    if not Path(PGADMIN_DB).exists():
        print(f"pgAdmin database not yet created at {PGADMIN_DB}")
        return False
    
    try:
        conn = sqlite3.connect(PGADMIN_DB)
        cursor = conn.cursor()
        
        # Check if server already exists
        cursor.execute("SELECT id FROM server WHERE name = ?", (SERVER_CONFIG["name"],))
        existing = cursor.fetchone()
        
        if existing:
            print(f"Server '{SERVER_CONFIG['name']}' already configured")
            conn.close()
            return True
        
        # Insert server configuration
        # Note: user_id (1) and connect_now (1) are hard-coded for default pgAdmin setup.
        # These values are required for initial configuration and match the default admin user.
        cursor.execute("""
            INSERT INTO server (
                user_id, servergroup_id, name, host, port, 
                maintenance_db, username, password, ssl_mode, 
                connect_now, comment
            ) VALUES (
                1, ?, ?, ?, ?,
                ?, ?, ?, ?,
                1, 'Auto-configured Confradar database'
            )
        """, (
            SERVER_CONFIG["group"],
            SERVER_CONFIG["name"],
            SERVER_CONFIG["host"],
            SERVER_CONFIG["port"],
            SERVER_CONFIG["maintenance_db"],
            SERVER_CONFIG["username"],
            SERVER_CONFIG["password"],  # pgAdmin will encrypt this
            SERVER_CONFIG["ssl_mode"],
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✓ Server '{SERVER_CONFIG['name']}' configured successfully")
        return True
        
    except Exception as e:
        print(f"Error configuring server: {e}")
        return False


if __name__ == "__main__":
    import time
    
    # Wait up to 30 seconds for pgAdmin to initialize
    for _ in range(30):
        if setup_server():
            break
        time.sleep(1)
    else:
        print("Failed to configure server after 30 seconds")
