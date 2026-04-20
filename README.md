# Flask HTTPS Database Viewer

Flask app that serves PostgreSQL data over HTTPS and renders it in a simple frontend page.

## What this project does
- Runs a Flask API and page over TLS (HTTPS)
- Exposes database data at `/database` and `/employees`
- Includes scripts for local certificate generation and VM startup

## Project files
- `app.py`: Flask routes and PostgreSQL access
- `test.html`: frontend page that loads database data
- `run_ssl.py`: Gunicorn HTTPS entrypoint
- `setup_https_local.sh`: generates self-signed cert/key with SANs
- `start_https_vm.sh`: starts HTTPS service and performs health check
- `database_dump.sql`: PostgreSQL schema + data export

## Quick start
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Configure database settings:
   - copy `.env.example` to `.env` and update values
   - or export `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
4. Start HTTPS server:
   - `./start_https_vm.sh`
5. Open in browser:
   - inside VM: `https://127.0.0.1:5000`
   - host with VirtualBox port-forwarding: `https://127.0.0.1:5443` (or configured host port)

## API endpoints
- `GET /`: returns the frontend page
- `GET /database`: returns all public tables and rows
- `GET /employees`: returns employees table rows
- `POST /employees`: inserts a new employee

## Deployment and security checklist
See `DEPLOYMENT_CHECKLIST.md` before sharing or deploying this app.

## Important notes
- Self-signed certificates show browser trust warnings until the cert is trusted by the host OS.
- Never commit `.env`, private keys, or credentials.
