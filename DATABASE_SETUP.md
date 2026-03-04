# SUCHANA HUB - PostgreSQL Database Setup (Windows Only)

This script automates PostgreSQL database setup on Windows.

## Prerequisites
- PostgreSQL installed and running
- PostgreSQL bin folder in PATH
- Administrator access to PostgreSQL

## Usage

Run this in PowerShell as Administrator:

```powershell
# Navigate to project directory
cd "C:\Users\di\Desktop\Suchana Hub"

# Run setup script
.\setup_database.ps1
```

## What it does:
1. Creates 'suchana_hub' database
2. Creates 'suchana_user' with password 'suchana_password'
3. Grants necessary privileges
4. Creates all tables with proper relationships
5. Creates indexes for performance
6. Inserts default settings

## Manual Setup (if script doesn't work):

```powershell
# Open PostgreSQL command line
psql -U postgres

# Execute these commands:
CREATE USER suchana_user WITH PASSWORD 'suchana_password';
CREATE DATABASE suchana_hub;
GRANT ALL PRIVILEGES ON DATABASE suchana_hub TO suchana_user;

# Then from your project directory:
python run.py
```

For more details, see SETUP_GUIDE.md
