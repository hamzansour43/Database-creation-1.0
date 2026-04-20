# Deployment and Security Checklist

Use this checklist before publishing or deploying.

## Source control safety
- [ ] `.env` is not committed
- [ ] `key.pem` is not committed
- [ ] `cert.pem` is not committed
- [ ] No hardcoded passwords or API keys in code
- [ ] Old leaked PAT tokens are revoked in GitHub

## Runtime configuration
- [ ] DB credentials are provided through environment variables
- [ ] `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` are set correctly
- [ ] Flask app can connect to PostgreSQL

## HTTPS setup
- [ ] Certificate and key exist on server runtime only
- [ ] HTTPS endpoint responds: `https://127.0.0.1:5000`
- [ ] Browser can reach VM endpoint through configured networking
- [ ] For production: use a trusted CA certificate (not self-signed)

## VirtualBox / VM networking
- [ ] VM server is running via `./start_https_vm.sh`
- [ ] Port-forwarding rule maps host port to guest HTTPS port
- [ ] Host browser opens the forwarded HTTPS URL

## Verification
- [ ] `GET /` returns 200
- [ ] `GET /database` returns data
- [ ] Frontend page displays database rows

## Before production
- [ ] Replace default credentials
- [ ] Restrict CORS to trusted origins only
- [ ] Put app behind a reverse proxy (Nginx/Apache)
- [ ] Add monitoring and log rotation
