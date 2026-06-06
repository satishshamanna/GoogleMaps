import os
from datetime import date
import requests
from dotenv import load_dotenv

def scrape_google_maps(service: str, city: str, count: int) -> list:
    """
    Searches Google Maps for a service in a city using the Places API (New) and returns exactly `count` leads.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY is not set in the environment or .env file.")

    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.websiteUri,places.rating"
    }

    # Places API (New) supports maxResultCount between 1 and 20.
    # We cap it at 20 for a single request.
    max_results = min(max(count, 1), 20)

    payload = {
        "textQuery": f"{service} in {city}",
        "maxResultCount": max_results
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch from Places API (New): {e}")

    places = data.get("places", [])
    leads = []
    today_str = date.today().isoformat()

    for place in places:
        if len(leads) >= count:
            break

        name = place.get("displayName", {}).get("text", "Unknown")
        address = place.get("formattedAddress", "Unknown")
        website = place.get("websiteUri")
        rating = place.get("rating")

        leads.append({
            "name": name,
            "service": service,
            "address": address,
            "website": website if website else None,
            "rating": float(rating) if rating is not None else None,
            "date_created": today_str,
            "status": "lead"
        })

    return leads
