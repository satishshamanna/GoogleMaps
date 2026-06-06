# scrape_google_maps Workflow

This workflow searches Google Maps for a specific service in a specified city, extracts business details, and returns a list of lead dictionaries.

## Logic Steps

1. **Format Search Query**: Combine `service` and `city` into a single query string: `"{service} in {city}"`.
2. **Execute Text Search**: Use the Google Maps Places API to run a text search query.
3. **Parse Candidates**: Retrieve the list of place search results. For each candidate:
   - Extract the `place_id`.
   - Call the Google Maps Place Details API to fetch extended details:
     - `name`
     - `formatted_address` (used as `address`)
     - `website` (if available)
     - `rating` (if available)
4. **Build Lead Records**: Construct a structured lead dictionary for each candidate with the following fields:
   - `name`: Business name (string)
   - `service`: The service searched for (string)
   - `address`: Full address (string)
   - `website`: Website URL (string or `None` if not available)
   - `rating`: Rating (float or `None` if not available)
   - `date_created`: Date scraped in ISO 8601 format (`YYYY-MM-DD`)
   - `status`: Default string `"lead"`
5. **Enforce Lead Count**: Retrieve and process place details until exactly `count` leads are successfully gathered (or all search results are processed if fewer than `count` exist).
6. **Return Output**: Return the list of leads.
