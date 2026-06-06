# Telegram Chatbot Workflow & Deployment

This workflow details how the Telegram chatbot is structured, how it parses natural language inputs using Gemini, and how it is deployed on Modal.

## System Architecture

1. **Telegram Webhook**: Modal hosts a FastAPI instance exposing a `/webhook` endpoint. Telegram sends message updates to this endpoint.
2. **Intent Parsing (Gemini)**: The webhook passes the user query to Gemini (`gemini-1.5-flash`) with instruction to classify intent and extract parameters as JSON.
3. **Workflow Dispatcher**: Based on the returned JSON, the chatbot invokes:
   - `scrape_google_maps` + `airtable_save_leads`
   - `airtable_search_leads`
4. **Telegram Response**: The bot formats the workflow results into Markdown and sends them back to the user via Telegram's sendMessage API.

## Modal Deployment Steps

### Step 1: Set Up Modal Secrets
Create a secret group named `googlemaps-secrets` in your Modal dashboard or via CLI containing:
- `TELEGRAM_BOT_TOKEN`
- `GEMINI_API_KEY`
- `GOOGLE_MAPS_API_KEY`
- `AIRTABLE_API_TOKEN`
- `AIRTABLE_BASE_ID`
- `AIRTABLE_TABLE_NAME`

### Step 2: Deploy to Modal
Run the following command to deploy the app:
```bash
modal deploy execution/chatbot.py
```
This will output a live web endpoint URL (e.g. `https://<org>-googlemaps-chatbot-fastapi-app.modal.run`).

### Step 3: Register the Webhook URL with Telegram
Set your webhook by calling the Telegram API:
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/setWebhook?url=https://<your-modal-app-domain>/webhook"
```
Verify the webhook is active by opening:
`https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/getWebhookInfo`
