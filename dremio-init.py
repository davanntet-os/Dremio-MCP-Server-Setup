#!/usr/bin/env python3
"""One-shot init: bootstrap Dremio's first admin user (if needed) and write a
fresh PAT to /shared/pat.txt for the dremio-mcp service to consume."""

import json
import os
import time
import urllib.request

URI = os.environ.get("DREMIO_URI", "http://dremio:9047").rstrip("/")
USER = os.environ.get("DREMIO_USER", "dremioadmin")
PASSWORD = os.environ.get("DREMIO_PASSWORD", "dremio123")
OUT = os.environ.get("PAT_FILE", "/shared/pat.txt")


def call(path, payload, method="POST"):
    req = urllib.request.Request(
        URI + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.load(resp)
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


print(f"Bootstrapping first user '{USER}' on {URI} (ignored if already done)")
r = call(
    "/apiv2/bootstrap/firstuser",
    {
        "userName": USER,
        "password": PASSWORD,
        "firstName": "Dremio",
        "lastName": "Admin",
        "email": "admin@local",
    },
    method="PUT",
)
print(f"bootstrap result: {r.get('userName', r.get('error'))}")

for attempt in range(60):
    r = call("/apiv2/login", {"userName": USER, "password": PASSWORD})
    token = r.get("token") if isinstance(r, dict) else None
    if token:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(token + "\n")
        os.chmod(OUT, 0o644)
        print(f"PAT written to {OUT}")
        break
    print(f"login attempt {attempt + 1} failed: {r.get('error', 'no token')}, retrying")
    time.sleep(5)
else:
    raise SystemExit("ERROR: could not obtain PAT from Dremio")
