# Walkthrough - Google Maps Lead Generation Telegram Chatbot

Here is a summary of the implementation details, verification steps, and active live links.

## What Was Completed

1. **Google Maps Scraper**:
   - Implemented `scrape_google_maps()` using the modern Google Places API (New) in [scrape_google_maps.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/scrape_google_maps.py).
   - Created workflow instructions in [scrape_google_maps.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/scrape_google_maps.md).
   - Added website homepage crawler in [scrape_google_maps.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/scrape_google_maps.py) that extracts contact emails and phone numbers.
   - Refined contact extraction:
     - Parses `href="mailto:..."` and `href="tel:..."` links first for high-precision results.
     - Strips `<script>`, `<style>`, and other HTML tags before executing regex fallbacks on clean text.
     - Prevents false-positive digits (like Shopify/Squarespace URL version numbers or timestamps) by filtering out long solid sequences of digits unless formatted or starting with `+`.
2. **Local Scraper Verification**:
   - Verified scraping and extraction on Toronto coffee shops, extracting correct emails and formatted phone numbers (e.g. `info@nabulucoffee.ca` and `(647) 669-1372`) and avoiding false positives.
3. **Airtable Save Leads**:
   - Implemented `airtable_save_leads()` in [airtable_save_leads.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/airtable_save_leads.py) using the official `pyairtable` library, supporting automatic batching (up to 10 records per request).
   - Mapped scraped email and phone numbers to Airtable `email` and `phone_number` columns.
   - Created [airtable_save_leads.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/airtable_save_leads.md) for workflow logic.
4. **Airtable Search Leads**:
   - Implemented `airtable_search_leads()` in [airtable_search_leads.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/airtable_search_leads.py) to search matching leads using Airtable formulas and sort by rating descending.
   - Mapped returned columns `email` and `phone_number` (renamed to `phone` in dicts).
   - Created [airtable_search_leads.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/airtable_search_leads.md) for workflow logic.
5. **Airtable Verification**:
   - Successfully verified by saving leads to Airtable and checking that email and phone_number columns were correctly populated and retrieved.
6. **Chatbot Webhook**:
   - Implemented [chatbot.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/chatbot.py) which sets up the Modal app, mounts local code, uses Gemini (`gemini-3.5-flash`) for intent and parameter parsing, and calls the corresponding workflow.
   - Implemented async FastAPI `BackgroundTasks` to respond instantly to Telegram webhook requests, preventing read timeout errors.
   - Updated response formatting in [chatbot.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/chatbot.py) to show extracted email and phone numbers in the Telegram message.
   - Created [chatbot.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/chatbot.md) describing the chatbot webhook flow.
7. **Modal Deployment**:
   - Deployed the chatbot FastAPI app to Modal at:
     `https://satishchannar--googlemaps-chatbot-fastapi-app.modal.run`
   - Configured `.env` file with Modal credentials (`MODAL_TOKEN_ID` and `MODAL_TOKEN_SECRET`) to ensure local execution/deploy command line authentication works out-of-the-box.
   - Registered the Telegram webhook to the Modal endpoint.
