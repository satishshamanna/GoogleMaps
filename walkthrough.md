# Walkthrough - Google Maps Lead Generation Telegram Chatbot

Here is a summary of the implementation details, verification steps, and active live links.

## What Was Completed

1. **Google Maps Scraper**:
   - Implemented `scrape_google_maps()` using the modern Google Places API (New) in [scrape_google_maps.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/scrape_google_maps.py).
   - Created workflow instructions in [scrape_google_maps.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/scrape_google_maps.md).
2. **Local Scraper Verification**:
   - Successfully verified by scraping 2 coffee shops in Toronto and saving them to [.tmp/leads.csv](file:///d:/SatishAIProjects/05-GoogleMap/.tmp/leads.csv).
3. **Airtable Save Leads**:
   - Implemented `airtable_save_leads()` in [airtable_save_leads.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/airtable_save_leads.py) using the official `pyairtable` library, supporting automatic batching (up to 10 records per request).
   - Created [airtable_save_leads.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/airtable_save_leads.md) for workflow logic.
4. **Airtable Search Leads**:
   - Implemented `airtable_search_leads()` in [airtable_search_leads.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/airtable_search_leads.py) to search matching leads using Airtable formulas and sort by rating descending.
   - Created [airtable_search_leads.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/airtable_search_leads.md) for workflow logic.
5. **Airtable Verification**:
   - Successfully verified by saving 5 software companies in Whitefield, Bangalore to Airtable.
6. **Chatbot Webhook**:
   - Implemented [chatbot.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/chatbot.py) which sets up the Modal app, mounts local code, uses Gemini (`gemini-1.5-flash`) for intent and parameter parsing, and calls the corresponding workflow.
   - Created [chatbot.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/chatbot.md) describing the chatbot webhook flow.
7. **Modal Deployment**:
   - Logged into Modal and created `googlemaps-secrets` with all 6 keys.
   - Deployed the chatbot FastAPI app to Modal at:
     `https://satishchannar--googlemaps-chatbot-fastapi-app.modal.run`
   - Registered the Telegram webhook to the Modal endpoint.

---

## Live Bot Verification

The bot is live and the webhook is active!

### How to test:
1. Open your Telegram app and open the chat with your bot: [t.me/googlemaps_leads_bot](https://t.me/googlemaps_leads_bot) (or your chosen bot username).
2. Send:
   `Find 5 plumbers in Miami`
3. **Expected behavior**:
   * The bot will reply: `Scraping Google Maps for 5 'plumber' leads in Miami...`
   * The bot will save the 5 leads to your Airtable table.
   * The bot will reply with a detailed review of the top results (Names, Ratings, Addresses, and Websites).
4. Send a search request to verify Airtable retrieval:
   `Search for software companies in Whitefield with minimum rating 4.5`
5. **Expected behavior**:
   * The bot will query Airtable and list the top results matching your criteria (e.g. the 5 software companies we uploaded during local testing).
