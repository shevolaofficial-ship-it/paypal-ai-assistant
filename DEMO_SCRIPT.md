# Demo Video Script (< 3 minutes)

## Setup (before recording)
1. Set environment variables:
   ```powershell
   $env:PAYPAL_CLIENT_ID="your_sandbox_client_id"
   $env:GEMINI_API_KEY="your_gemini_key"
   python app.py
   ```
2. Open http://127.0.0.1:8080 in browser.
3. Have PayPal sandbox buyer credentials ready.

## Script

### [0:00-0:15] Introduction
- Show the app homepage.
- "This is PayPal AI Assistant — it combines PayPal payments with AI to explain transactions in plain language."

### [0:15-0:45] PayPal Checkout
- Click the PayPal button.
- Log in with sandbox buyer account.
- Complete the $25.00 payment.
- Show "Payment captured" message.

### [0:45-1:15] AI Explanation
- The payment details auto-fill the textarea.
- Click "Explain with AI".
- Show the AI generating an explanation (may take 30-60s).
- Read the explanation aloud: what happened, risks, next steps.

### [1:15-1:45] Manual Query
- Type a custom question: "I sent $50 to a new merchant. Is this risky?"
- Click "Explain with AI".
- Show the AI response.

### [1:45-2:00] Health Check
- Open http://127.0.0.1:8080/health in a new tab.
- Show the JSON response confirming configuration.

### [2:00-2:30] Code Walkthrough
- Show app.py briefly: gemini_explain function, PayPal SDK integration.
- Highlight: "No external dependencies, stdlib only."

### [2:30-3:00] Closing
- "PayPal AI Assistant: payments you can understand. Built with PayPal + Gemini AI."
- Show GitHub repo link (once created).

## Tips
- Keep it under 3 minutes.
- Use screen recording (OBS or Windows Game Bar: Win+G).
- Speak clearly; the AI explanation may take time — edit out the wait.
- Upload to YouTube as public/unlisted.
