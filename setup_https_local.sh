#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

HOSTNAME_SHORT="$(hostname -s 2>/dev/null || echo localhost)"
HOSTNAME_FQDN="$(hostname -f 2>/dev/null || echo localhost)"

IPV4_LIST="$(hostname -I 2>/dev/null | tr ' ' '\n' | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$' || true)"

TMP_CONF="$(mktemp)"

cat > "$TMP_CONF" <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
x509_extensions = v3_req
distinguished_name = dn

[dn]
CN = ${HOSTNAME_SHORT}

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = ${HOSTNAME_SHORT}
DNS.3 = ${HOSTNAME_FQDN}
IP.1 = 127.0.0.1
IP.2 = ::1
EOF

index=3
while IFS= read -r ip; do
  if [[ -n "$ip" ]]; then
    echo "IP.${index} = ${ip}" >> "$TMP_CONF"
    index=$((index + 1))
  fi
done <<< "$IPV4_LIST"

echo "Generating self-signed TLS certificate with SAN entries..."
openssl req -x509 -nodes -days 825 -newkey rsa:2048 \
  -keyout key.pem \
  -out cert.pem \
  -config "$TMP_CONF" \
  -extensions v3_req

chmod 600 key.pem
chmod 644 cert.pem

rm -f "$TMP_CONF"

echo "Done. Generated files:"
echo "  cert.pem"
echo "  key.pem"
echo
echo "Certificate SANs:"
openssl x509 -in cert.pem -noout -ext subjectAltName

echo
echo "Next:"
echo "  1) Start HTTPS app: python run_ssl.py"
echo "  2) Open: https://<your-vm-ip>:5000"
