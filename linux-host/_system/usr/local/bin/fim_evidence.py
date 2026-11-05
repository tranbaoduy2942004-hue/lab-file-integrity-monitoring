#!/usr/bin/env python3
import json
import hashlib
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE = Path("/home/ubuntu/fim-lab")
CFG = BASE / "app.conf"
BACKUP = BASE / "baseline.conf"
ACTIONS = BASE / "actions.log"

def sha256(path):
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_file(path):
    return path.read_text() if path.exists() else ""

def get_evidence():
    return {
        "baseline_hash": sha256(BACKUP),
        "current_hash": sha256(CFG),
        "baseline_config": read_file(BACKUP),
        "current_config": read_file(CFG),
        "actions": read_file(ACTIONS)
    }

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.client_address[0] != "172.29.115.20":
            self.send_error(403)
            return

        if self.path != "/state":
            self.send_error(404)
            return

        raw = json.dumps(get_evidence()).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *args):
        pass

print("FIM_EVIDENCE_API_READY", flush=True)
HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
