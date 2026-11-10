# PayPal AI Assistant

Hackathon starter for the **PayPal AI Hackathon** (deadline 2026-11-12, Devpost).

Meaningfully combines:
- **PayPal** payments (sandbox checkout button + capture)
- **AI** (Gemini explains a payment/transaction in plain language)

## Health check

After starting the server, verify it is running:

```powershell
Invoke-WebRequest http://127.0.0.1:8080/health
```

Expected response: `{"status": "ok", "gemini_key": "set", "paypal_client_id": "set"}` (or "missing" if keys are not configured).

## Quick start

1. Install Python 3.11+ (already present on this machine).
2. Create a PayPal Developer sandbox account and an app (https://developer.paypal.com).
   Copy the **Sandbox Client ID**.
3. Get a Gemini API key (https://aistudio.google.com/apikey).
4. Set environment variables and run:

   ```powershell
   $env:PAYPAL_CLIENT_ID="your_sandbox_client_id"
   $env:GEMINI_API_KEY="your_gemini_key"
   python app.py
   ```
   Then open http://127.0.0.1:8080

## What to submit (Devpost)

- Public GitHub repo with all source + a LICENSE file at the top.
- Text description of features.
- Functional demo: either hosted URL or clear run instructions (this README qualifies).
- Demo video under 3 minutes on YouTube (public).
- Identify which AI tool was used and how (Gemini, for payment explanation).

## Submission materials (ready)

- `DEVPOST_SUBMISSION.md` — full Devpost submission text (copy-paste ready).
- `DEMO_SCRIPT.md` — step-by-step demo video script (<3 min).
- `LICENSE` — MIT license at top level.
- `.env.example` — environment variable template.

## Submission checklist (owner)

- [ ] Create Devpost account (https://secure.devpost.com/users/register)
- [ ] Join hackathon (https://paypalaihackathon.devpost.com/register)
- [ ] Create PayPal Developer sandbox app (https://developer.paypal.com) -> copy Sandbox Client ID into PAYPAL_CLIENT_ID
- [ ] Create GitHub account + `gh auth login` (device flow)
- [ ] Create repo, push this project, add LICENSE at top
- [ ] Record demo video (<3 min) showing: sandbox checkout + AI explanation
- [ ] Fill Devpost submission form (description, GitHub URL, video URL, tools used)
- [ ] Submit before 2026-11-12 12:00 PST

## Notes

- Sandbox only. No real money moves.
- No secrets are committed; keys come from environment variables.
- The PayPal button requires a real sandbox client id to render correctly.
