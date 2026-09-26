#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME=lago-stripe-invoice-idor
BASE="${1:-http://127.0.0.1:13001}"
chmod +x seed_stripe.rb

if [ -f poc.py ]; then
  POC=./poc.py
elif [ -f ../lago-stripe-invoice-idor-Abraxas-Labs.py ]; then
  POC=../lago-stripe-invoice-idor-Abraxas-Labs.py
else
  echo "FAIL no poc.py"
  exit 1
fi
chmod +x "$POC"

echo "== docker compose up (getlago/lago:v1.53.0, loopback) =="
docker compose up -d

echo "== wait for GraphQL =="
ok=0
for i in $(seq 1 90); do
  if curl -fsS -o /dev/null "$BASE/health"; then
    echo "IOC lago-up"
    ok=1
    break
  fi
  echo "IOC wait i=$i"
  sleep 3
done
if [[ "$ok" != 1 ]]; then
  echo "FAIL Lago API did not become ready on $BASE"
  docker compose logs --tail=80
  exit 1
fi
sleep 5

echo "== poc.py =="
python3 "$POC" "$BASE"
