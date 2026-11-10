#!/usr/bin/env python3
"""PayPal AI Assistant — hackathon starter.

Minimal, self-contained web app for the PayPal AI Hackathon.
- Serves a page with a PayPal sandbox checkout button.
- Exposes /api/explain which uses Gemini to explain a payment/transaction.

Run:
    set GEMINI_API_KEY=your_key
    set PAYPAL_CLIENT_ID=your_sandbox_client_id
    python app.py
Then open http://127.0.0.1:8080
"""
from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8080"))
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID", "YOUR_PAYPAL_SANDBOX_CLIENT_ID")


def gemini_explain(text: str) -> str:
    if not GEMINI_KEY:
        return "GEMINI_API_KEY is not set; cannot generate an AI explanation."
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-flash-latest:generateContent?key={urllib.parse.quote(GEMINI_KEY)}"
    )
    body = {
        "contents": [{"parts": [{"text": (
            "You are a helpful payments assistant. Explain the following payment or "
            "transaction in plain language, note any risks or next steps, and keep it "
            "under 120 words.\n\n" + text
        )}]}],
        "generationConfig": {"maxOutputTokens": 120, "temperature": 0.3},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    last_err = None
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
            cand = data.get("candidates", [{}])[0]
            parts = cand.get("content", {}).get("parts", [])
            reply = "".join(p.get("text", "") for p in parts).strip()
            if reply:
                return reply
            return "No response from AI."
        except Exception as e:  # noqa: BLE001
            last_err = e
            if attempt == 0:
                time.sleep(2)
    # Fallback: provide a helpful static explanation when AI is unavailable
    return (
        "AI explanation unavailable (Gemini timed out). Here is a general guide:\n"
        "- Verify the payment amount and recipient are correct.\n"
        "- Check for any unexpected fees or currency conversion.\n"
        "- Confirm the transaction appears in your PayPal activity.\n"
        "- If anything looks wrong, contact PayPal support or the merchant.\n"
        "Tip: retry in a few minutes when the AI service is less busy."
    )


INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PayPal AI Assistant</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 720px; margin: 40px auto; padding: 0 16px; }
  h1 { margin-bottom: 4px; }
  .card { border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin: 16px 0; }
  #explain-out { white-space: pre-wrap; background: #f6f8fa; padding: 12px; border-radius: 8px; min-height: 60px; }
  textarea { width: 100%; box-sizing: border-box; }
  button { padding: 8px 14px; border-radius: 8px; border: 1px solid #ccc; cursor: pointer; }
  #paypal-button-container { margin: 12px 0; }
</style>
</head>
<body>
  <h1>PayPal AI Assistant</h1>
  <p>Meaningfully combines <strong>PayPal payments</strong> with <strong>AI</strong>: pay with PayPal in the sandbox, then ask the AI to explain the payment.</p>

  <div class="card">
    <h3>1. Pay with PayPal (sandbox)</h3>
    <div id="paypal-button-container"></div>
    <p style="font-size:12px;color:#666">Replace YOUR_PAYPAL_SANDBOX_CLIENT_ID in app.py with your sandbox client id.</p>
  </div>

  <div class="card">
    <h3>2. Ask the AI about a payment</h3>
    <textarea id="q" rows="4" placeholder="e.g. I just sent $25.00 to merchant X for an invoice. What should I check?"></textarea>
    <div style="margin:8px 0"><button id="go">Explain with AI</button></div>
    <div id="explain-out">AI explanation will appear here.</div>
  </div>

  <script src="https://www.paypal.com/sdk/js?client-id=__CLIENT_ID__&currency=USD&intent=capture"></script>
  <script>
    if (window.paypal) {
      paypal.Buttons({
        createOrder: (data, actions) => actions.order.create({ purchase_units: [{ amount: { value: '25.00' } }] }),
        onApprove: (data, actions) => actions.order.capture().then(details => {
          const name = (details.payer && details.payer.name && details.payer.name.given_name) || 'buyer';
          document.getElementById('q').value = 'Payment captured for $25.00 from ' + name + '. Order id: ' + data.orderID;
          document.getElementById('explain-out').textContent = 'Payment captured. Ask the AI to explain it.';
        })
      }).render('#paypal-button-container');
    }
    document.getElementById('go').onclick = async () => {
      const text = document.getElementById('q').value.trim();
      if (!text) return;
      const out = document.getElementById('explain-out');
      out.textContent = 'Thinking...';
      try {
        const r = await fetch('/api/explain', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({text}) });
        const j = await r.json();
        out.textContent = j.reply || 'No reply.';
      } catch (e) { out.textContent = 'Error: ' + e; }
    };
  </script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str = "text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if self.path == "/health":
            status = {
                "status": "ok",
                "gemini_key": "set" if GEMINI_KEY else "missing",
                "paypal_client_id": "set" if PAYPAL_CLIENT_ID and PAYPAL_CLIENT_ID != "YOUR_PAYPAL_SANDBOX_CLIENT_ID" else "missing",
            }
            self._send(200, json.dumps(status).encode("utf-8"), "application/json")
        elif self.path == "/" or self.path == "/index.html":
            html = INDEX_HTML.replace("__CLIENT_ID__", PAYPAL_CLIENT_ID)
            self._send(200, html.encode("utf-8"))
        else:
            self._send(404, b"Not found", "text/plain")

    def do_POST(self):  # noqa: N802
        if self.path == "/api/explain":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                payload = json.loads(raw.decode("utf-8"))
            except Exception:
                payload = {}
            text = str(payload.get("text", "")).strip()
            reply = gemini_explain(text) if text else "Please provide text to explain."
            self._send(200, json.dumps({"reply": reply}).encode("utf-8"), "application/json")
        else:
            self._send(404, b"Not found", "text/plain")

    def log_message(self, fmt, *args):  # quieter logs
        pass


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"PayPal AI Assistant running at http://{HOST}:{PORT}")
    print(f"PayPal client id: {PAYPAL_CLIENT_ID}")
    print(f"Gemini key: {'set' if GEMINI_KEY else 'NOT SET'}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
