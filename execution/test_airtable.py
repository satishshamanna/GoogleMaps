import os
import csv
from airtable_save_leads import airtable_save_leads
from airtable_search_leads import airtable_search_leads

def test_airtable():
    csv_file = ".tmp/leads.csv"
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} does not exist. Run test_scraper.py first.")
        return

    # 1. Read leads from local CSV
    leads = []
    print(f"Reading leads from {csv_file}...")
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse rating back to float if present
            rating = row.get("rating")
            leads.append({
                "name": row.get("name"),
                "service": row.get("service"),
                "address": row.get("address"),
                "website": row.get("website") if row.get("website") else None,
                "rating": float(rating) if rating else None,
                "email": row.get("email") if row.get("email") else None,
                "phone": row.get("phone") if row.get("phone") else None,
                "date_created": row.get("date_created"),
                "status": row.get("status", "lead")
            })

    print(f"Read {len(leads)} leads. Uploading to Airtable...")

    # 2. Save leads to Airtable
    try:
        saved_count = airtable_save_leads(leads)
        print(f"Successfully saved {saved_count} leads to Airtable!")
    except Exception as e:
        print(f"Error saving to Airtable: {e}")
        return

    # 3. Search leads back from Airtable to verify search function
    print("Searching leads back from Airtable to verify read permissions...")
    try:
        results = airtable_search_leads(city="Toronto", count=5)
        print(f"Found {len(results)} leads in Airtable for Toronto:")
        for res in results:
            print(f"- {res['name']} (Rating: {res['rating']}, Website: {res['website']}, Email: {res['email']}, Phone: {res['phone']}, Status: {res['status']})")
    except Exception as e:
        print(f"Error searching Airtable: {e}")

if __name__ == "__main__":
    test_airtable()
