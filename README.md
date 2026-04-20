# Flask HTTPS Database Viewer

This project serves a Flask web page over HTTPS and shows PostgreSQL database data.

## Features
- HTTPS web server with self-signed TLS
- Database API endpoint at `/database`
- HTML page that renders table data

## Files
- `app.py`: Flask app and API routes
- `run_ssl.py`: Gunicorn HTTPS runner
- `start_https_vm.sh`: one-command startup for VM
- `setup_https_local.sh`: generates local TLS certs
- `test.html`: frontend page
- `database_dump.sql`: PostgreSQL export (schema + data)

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Configure database credentials:
   - copy `.env.example` to `.env` and update values
   - or export `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
4. Start HTTPS server:
   - `./start_https_vm.sh`

## Notes
- Self-signed certificates will show browser warnings until trusted.
- Do not commit `.env`, `key.pem`, or `cert.pem`.
