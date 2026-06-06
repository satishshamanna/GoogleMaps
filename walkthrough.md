# Walkthrough - Google Maps Lead Generation Telegram Chatbot

Here is a summary of the implementation details, verification steps, and how to proceed with Modal deployment.

## What Was Completed

1. **Google Maps Scraper**:
   - Implemented `scrape_google_maps()` using the modern Google Places API (New) in [scrape_google_maps.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/scrape_google_maps.py).
   - Created the corresponding workflow instructions in [scrape_google_maps.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/scrape_google_maps.md).
2. **Local Scraper Verification**:
   - Created a local verification script [test_scraper.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/test_scraper.py) which successfully queried 2 coffee shops in Toronto and saved them to [.tmp/leads.csv](file:///d:/SatishAIProjects/05-GoogleMap/.tmp/leads.csv).
3. **Airtable Save Leads**:
   - Implemented `airtable_save_leads()` in [airtable_save_leads.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/airtable_save_leads.py) using the official `pyairtable` library, supporting automatic batching (up to 10 records per request).
   - Created [airtable_save_leads.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/airtable_save_leads.md) for workflow logic.
4. **Airtable Search Leads**:
   - Implemented `airtable_search_leads()` in [airtable_search_leads.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/airtable_search_leads.py) to search matching leads using Airtable formulas and sort by rating descending.
   - Created [airtable_search_leads.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/airtable_search_leads.md) for workflow logic.
5. **Chatbot Webhook**:
   - Implemented [chatbot.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/chatbot.py) which sets up the Modal app, mounts local code, uses Gemini (`gemini-1.5-flash`) for intent and parameter parsing, and calls the corresponding workflow.
   - Created [chatbot.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/chatbot.md) describing the chatbot webhook flow and deployment commands.

---

## Local Scraper Test Output

The test script executed successfully and output the following leads:
```text
Scraping 2 coffee shops in Toronto...
Scraped 2 leads:
- Dineen Coffee Co. (Rating: 4.3, Website: https://www.dineencoffee.com/)
- NEO COFFEE BAR (Rating: 4.5, Website: https://www.neocoffeebar.com/location-frederick-x-king)
Successfully saved leads to .tmp/leads.csv
```

---

## Deployment & Verification Checklist

To complete the setup and run the live Telegram bot on Modal:

### 1. Fill in the Airtable Credentials
Open your [.env](file:///d:/SatishAIProjects/05-GoogleMap/.env) file and replace `your_airtable_pat` and `your_base_id` with your real Airtable credentials.

### 2. Set Up Modal Secrets
Create a secret group named `googlemaps-secrets` in your [Modal Dashboard](https://modal.com/) with the keys:
- `TELEGRAM_BOT_TOKEN`
- `GEMINI_API_KEY`
- `GOOGLE_MAPS_API_KEY`
- `AIRTABLE_API_TOKEN`
- `AIRTABLE_BASE_ID`
- `AIRTABLE_TABLE_NAME`

### 3. Deploy to Modal
Run the deployment command:
```bash
modal deploy execution/chatbot.py
```
This will output your web endpoint URL.

### 4. Link Webhook to Telegram
Call the Telegram API to register the webhook URL:
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/setWebhook?url=https://<your-modal-app-domain>/webhook"
```
Once linked, send `"Find 5 plumbers in Miami"` on Telegram to test the full end-to-end implementation!
