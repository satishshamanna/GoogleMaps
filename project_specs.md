# Project Specifications

## Inputs
The chatbot will receive messages from Telegram. The messages can be natural language queries such as:
- `"Find 5 plumbers in Miami"` (should trigger maps scraping and saving leads to Airtable)
- `"Search for plumbers in Miami with minimum rating 4"` (should trigger Airtable search and return results)

## Workflows
The system has exactly three core workflows:

1. **`scrape_google_maps`**
   - **Input**:
     - `service` (string, e.g., `"plumber"`)
     - `city` (string, e.g., `"Miami"`)
     - `count` (integer, e.g., `5`)
   - **Logic**:
     - Formulate a text search query: `"{service} in {city}"`.
     - Query Google Maps Places API (using the text search endpoint).
     - Retrieve `place_id` for the top results.
     - For each place, call the Places Details API to fetch:
       - `name`
       - `formatted_address` (used as `address`)
       - `website` (if available)
       - `rating` (if available)
     - Limit/slice the results to return exactly `count` leads.
   - **Output**: A list of lead dictionaries. Each lead must contain:
     - `name` (string)
     - `service` (string)
     - `address` (string)
     - `website` (string or `None`)
     - `rating` (float or `None`)
     - `date_created` (ISO 8601 date string, e.g., `"2026-06-06"`)
     - `status` (string, defaults to `"lead"`)

2. **`airtable_save_leads`**
   - **Input**: List of lead dicts (from `scrape_google_maps`).
   - **Logic**:
     - Authenticate with Airtable.
     - Map lead fields to Airtable table columns exactly (`name`, `service`, `address`, `website`, `rating`, `date_created`, `status`).
     - Insert/save each lead into the Airtable base/table.
   - **Output**: Success status indicating the number of leads successfully saved.

3. **`airtable_search_leads`**
   - **Input Filters**:
     - `city` (string, optional)
     - `service` (string, optional)
     - `minimum_rating` (float, optional)
     - `status` (string, optional)
     - `count` (integer, default `5`)
   - **Logic**:
     - Construct an Airtable filter formula using the provided criteria.
     - Fetch matching records.
     - Sort results by `rating` in descending order (highest first).
     - Return exactly `count` results (or fewer if not enough exist).
   - **Output**: List of lead records matching the filters.

## Tools & Integrations
* **Telegram Bot API**: For receiving user commands and sending chatbot replies.
  - **Bot Name**: `Maps Lead Gen Bot`
  - **Bot Username**: `@SS_Googlemaps_leads_bot`
* **Gemini API**: For natural language understanding to parse user intent, service, city, count, and minimum rating.
* **Google Maps Places API**: For scraping local business leads.
* **Airtable API**: For storing and searching lead records.
* **Modal**: Serverless cloud platform for deploying the chatbot webhook and executing workflows.

## Expected Outputs
* **Telegram Response**: Text messages confirming lead scraping/saving status or displaying search results.
* **Airtable Records**: Correctly populated rows in the designated Airtable base.

## Data Storage
* **Airtable**: Live lead database.
* **`.tmp/`**: Local cache directory for debugging/logs.

## Deployment
* **Modal Cloud**: Main application running as a FastAPI web endpoint for the Telegram webhook.
* **Modal Secrets**: For storing API keys securely:
  * `TELEGRAM_BOT_TOKEN`
  * `GEMINI_API_KEY`
  * `GOOGLE_MAPS_API_KEY`
  * `AIRTABLE_API_TOKEN`
  * `AIRTABLE_BASE_ID`
  * `AIRTABLE_TABLE_NAME`

## Definition of Done
When a user sends `"Find 5 plumbers in Miami"` on Telegram:
1. The chatbot parses the request using Gemini.
2. The chatbot scrapes 5 plumbers in Miami from Google Maps.
3. The chatbot saves all 5 leads to Airtable.
4. The chatbot sends a reply confirming completion.
5. The chatbot reviews the top results back to the user.
