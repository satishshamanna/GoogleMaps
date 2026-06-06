# Implementation Plan - Email & Phone Extraction from Lead Websites

This plan describes how we will implement email and phone number extraction from scraped business websites and integrate them into the lead generation workflow and Airtable database.

## User Review Required

> [!WARNING]
> You must create two new columns in your Airtable **Leads** table to store this data:
> 1. **`email`** (Single line text or Email type)
> 2. **`phone`** (Single line text or Phone number type)
>
> If you do not add these columns, the Airtable upload script will fail with an invalid column error.

## Proposed Changes

We will modify the existing workflow execution files to integrate the email and phone scraping logic.

---

### Google Maps Scraper Workflow

#### [MODIFY] [scrape_google_maps.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/scrape_google_maps.py)
- Implement `extract_contact_info(url)`:
  - Fetch the homepage of the website using `requests` with a 5-second timeout and custom User-Agent.
  - Use regex to search for email addresses: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
  - Use regex to search for phone numbers: `(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}`
  - Clean and filter extracted values.
- In `scrape_google_maps()`, after getting place details, call `extract_contact_info(website)` and add the extracted values as `email` and `phone` fields.

---

### Airtable Save & Search Workflows

#### [MODIFY] [airtable_save_leads.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/airtable_save_leads.py)
- Include `email` and `phone` fields in the record mapping dictionary.

#### [MODIFY] [airtable_search_leads.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/airtable_search_leads.py)
- Return `email` and `phone` in the returned search result dictionaries.

---

### Chatbot Webhook

#### [MODIFY] [chatbot.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/chatbot.py)
- Update the final response formatter to display the extracted email and phone numbers in the Telegram message:
  ```text
  1. Business Name (Rating: 4.8)
     📍 Address
     📧 Email: example@domain.com
     📞 Phone: 555-555-5555
     🔗 Website Link
  ```

---

## Verification Plan

### Manual Verification
1. Open Airtable and add columns: `email` and `phone`.
2. Update local test scripts:
   - [test_scraper.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/test_scraper.py): Verify that Toronto coffee shop scraping extracts emails/phones and saves them to `.tmp/leads.csv`.
   - [test_airtable.py](file:///d:/SatishAIProjects/05-GoogleMap/execution/test_airtable.py): Verify that leads with email/phone upload correctly.
3. Deploy the updated app:
   ```bash
   modal deploy execution/chatbot.py
   ```
4. Send `"Find 5 plumbers in Miami"` on Telegram to verify the live scraper, email/phone extraction, and Airtable storage.
