# Devpost Submission — PayPal AI Assistant

## Project Name
PayPal AI Assistant

## Tagline
Pay with PayPal in the sandbox, then let AI explain the payment in plain language.

## Inspiration
Payments are confusing. When users send or receive money, they often don't understand what just happened, what fees apply, or what risks exist. We wanted to combine PayPal's trusted payment infrastructure with AI to make payments transparent and understandable.

## What it does
1. **Pay with PayPal (sandbox):** A PayPal checkout button lets users complete a sandbox payment (no real money).
2. **AI explanation:** After payment, the user can ask the AI (Gemini) to explain the transaction in plain language — what happened, any risks, and next steps.
3. **Health check:** `/health` endpoint reports configuration status (Gemini key, PayPal client ID).

## How we built it
- **Backend:** Python (stdlib only, no external dependencies) — HTTP server with PayPal SDK integration and Gemini API for AI explanations.
- **Frontend:** Vanilla HTML/CSS/JS with PayPal JS SDK button.
- **AI:** Google Gemini (gemini-flash-latest) generates plain-language explanations of payments/transactions.
- **Payments:** PayPal Sandbox (client-side SDK + server-side capture).

## Challenges we ran into
- Gemini API latency from the test machine (30-60s per call). Mitigated with retry logic and reduced timeout.
- Embedded browser tunnel blocks GitHub/PayPal access. Used Python urllib for API calls instead.
- Low RAM (0.3 GB free) limited local tooling. Kept the app dependency-free (stdlib only).

## Accomplishments that we're proud of
- Fully self-contained app (no pip install needed).
- Meaningful PayPal + AI integration: not just a button, but AI that explains real payment data.
- Health check endpoint for easy deployment verification.

## What we learned
- Combining payment APIs with AI creates immediate user value.
- Keeping dependencies minimal makes deployment trivial.

## What's next for PayPal AI Assistant
- Add transaction history and multi-currency support.
- Integrate PayPal webhooks for real-time payment notifications.
- Add voice input for accessibility.
- Support multiple AI providers (OpenAI, Anthropic) as fallbacks.

## Built With
- Python
- PayPal (Sandbox)
- Google Gemini
- HTML/CSS/JavaScript

## Try it out
- GitHub: [to be added after repo creation]
- Live demo: [to be added after deployment]

## AI Tool Used
- **Google Gemini** (gemini-flash-latest) — used to generate plain-language explanations of payment transactions. The `/api/explain` endpoint sends payment text to Gemini and returns a concise explanation (<120 words) with risk notes.
