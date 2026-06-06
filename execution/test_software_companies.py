import os
from scrape_google_maps import scrape_google_maps
from airtable_save_leads import airtable_save_leads

def test_run():
    service = "software company"
    city = "Whitefield, Bangalore"
    count = 5
    
    print(f"Scraping {count} '{service}' leads in '{city}'...")
    try:
        leads = scrape_google_maps(service, city, count)
        print(f"Scraped {len(leads)} leads successfully.")
        for i, lead in enumerate(leads, start=1):
            print(f"{i}. {lead['name']} | Rating: {lead['rating']} | Address: {lead['address']}")
            
        if not leads:
            print("No leads scraped. Check API status or search term.")
            return
            
        print("Uploading to Airtable...")
        saved_count = airtable_save_leads(leads)
        print(f"Successfully saved {saved_count} leads to Airtable!")
    except Exception as e:
        print(f"Error occurred during test: {e}")

if __name__ == "__main__":
    test_run()
