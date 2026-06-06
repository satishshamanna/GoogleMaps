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
   - Implemented [chatbot.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/chatbot.py) which sets up the Modal app, mounts local code, uses Gemini (`gemini-3.5-flash`) for intent and parameter parsing, and calls the corresponding workflow.
   - Implemented async FastAPI `BackgroundTasks` to respond instantly to Telegram webhook requests, preventing read timeout errors.
   - Created [chatbot.md](file:///d:/SatishAIProjects/05-GoogleMap/instructions/chatbot.md) describing the chatbot webhook flow.
7. **Modal Deployment**:
   - Logged into Modal and created `googlemaps-secrets` with all 6 keys.
   - Deployed the chatbot FastAPI app to Modal at:
     `https://satishchannar--googlemaps-chatbot-fastapi-app.modal.run`
   - Registered the Telegram webhook to the Modal endpoint.

---

## Live Verification Results

The end-to-end flow was verified successfully!

### Test Case: "Find 5 plumbers in Miami"
1. **Telegram Request**: Sent `"Find 5 plumbers in Miami"` to the bot chat at [t.me/SS_Googlemaps_leads_bot](https://t.me/SS_Googlemaps_leads_bot).
2. **Instant Status Response**: Bot immediately replied:
   > 🔍 **Scraping Google Maps** for 5 'plumber' leads in Miami...
3. **Execution**: Scraped 5 leads and stored them to Airtable.
4. **Final Response**: Bot reviewed the top results and confirmed completion on Telegram:
   > ✅ **Successfully saved 5 leads to Airtable!**
   > 
   > Here is a review of the top results:
   > 1. **Miami 305 Plumbing** (⭐ 5.0)
   >    📍 11025 SW 56th St, Miami, FL 33165, USA
   >    🔗 [Website](https://miami305plumbing.com/)
   > 2. **Miami Dade Plumbing** (⭐ 4.9)
   >    📍 9417 SW 77th Ct, Miami, FL 33156, USA
   >    🔗 [Website](https://miami-dade-plumbing.com/)
   > 3. **Miami 24/7 Plumbing - Miami Emergency Plumbers** (⭐ 4.9)
   >    📍 1331 SW 32nd Ave #4, Miami, FL 33145, USA
   >    🔗 [Website](https://www.miami247plumbing.com/)
   > 4. **Sunny Bliss Plumbing & Air** (⭐ 4.9)
   >    📍 605 Lincoln Rd Suite 250B, Miami Beach, FL 33139, USA
   >    🔗 [Website](https://sunnybliss.com/)
   > 5. **Roto-Rooter Plumbing & Water Cleanup** (⭐ 4.7)
   >    📍 1726 NW 36th St Unit 3, Miami, FL 33142, USA
   >    🔗 [Website](https://www.rotorooter.com/miami/?...)
5. **Airtable Status**: Verified that all 5 leads were correctly inserted with their respective `name`, `service`, `address`, `website`, `rating`, `date_created`, and `status`.
