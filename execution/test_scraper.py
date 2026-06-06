import os
import csv
from scrape_google_maps import scrape_google_maps

def test():
    # Make sure .tmp directory exists
    os.makedirs(".tmp", exist_ok=True)
    
    print("Scraping 2 coffee shops in Toronto...")
    try:
        leads = scrape_google_maps("coffee shop", "Toronto", 2)
        print(f"Scraped {len(leads)} leads:")
        for lead in leads:
            print(f"- {lead['name']} (Rating: {lead['rating']}, Website: {lead['website']}, Email: {lead['email']}, Phone: {lead['phone']})")
        
        csv_file = ".tmp/leads.csv"
        fields = ["name", "service", "address", "website", "rating", "email", "phone", "date_created", "status"]
        
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for lead in leads:
                writer.writerow(lead)
                
        print(f"Successfully saved leads to {csv_file}")
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test()
