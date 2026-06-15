#!/usr/bin/env python3
"""Decision sheet server for the-vault.
GET  : serves this decisions/ directory (every *.html sheet) on 127.0.0.1:8910.
POST /decision : writes the operator's picks + comment to decisions/inbox/<ts>.json
                 AND mirrors the latest to decisions/inbox/LATEST.json, so the agent
                 reads the decision automatically — the operator never copy-pastes.
Bind: 127.0.0.1:8910 (localhost only)."""
import json, os, datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(ROOT, "inbox")
os.makedirs(INBOX, exist_ok=True)

class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def log_message(self, *a):
        pass
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        if self.path == "/decision":
            body = ""
            try:
                n = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(n).decode("utf-8")
                data = json.loads(body)
            except Exception as e:
                data = {"error": str(e), "raw": body}
            data["_received_at"] = datetime.datetime.now().isoformat(timespec="seconds")
            ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            with open(os.path.join(INBOX, "decision-%s.json" % ts), "w") as f:
                json.dump(data, f, indent=2)
            with open(os.path.join(INBOX, "LATEST.json"), "w") as f:
                json.dump(data, f, indent=2)
            self.send_response(200)
            self.send_header("Content-Type", "application/json"); self._cors(); self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404); self.end_headers()

if __name__ == "__main__":
    print("decision-server on http://127.0.0.1:8910/  (inbox: %s)" % INBOX)
    ThreadingHTTPServer(("127.0.0.1", 8910), H).serve_forever()
