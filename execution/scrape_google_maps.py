import os
import re
from datetime import date
import requests
from dotenv import load_dotenv

def extract_contact_info(url: str) -> tuple:
    """
    Fetches the website URL and attempts to extract email and phone number.
    Returns (email, phone) as a tuple.
    """
    if not url:
        return None, None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return None, None

        text = response.text

        # 1. Search href links first for high confidence matches
        mailto_links = re.findall(r'href=["\']mailto:([^"\']+)["\']', text, re.IGNORECASE)
        tel_links = re.findall(r'href=["\']tel:([^"\']+)["\']', text, re.IGNORECASE)

        link_emails = []
        for m in mailto_links:
            email_clean = m.split("?")[0].strip()
            if email_clean:
                link_emails.append(email_clean)

        link_phones = []
        for t in tel_links:
            phone_clean = t.split("?")[0].strip()
            # keep only valid characters (digits, +, -, (, ))
            phone_clean = re.sub(r'[^\d+\-\(\)\s]', '', phone_clean)
            if phone_clean:
                link_phones.append(phone_clean)

        # 2. Search clean text fallback
        # Strip script and style tags
        clean_text = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', ' ', text, flags=re.IGNORECASE)
        clean_text = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', ' ', clean_text, flags=re.IGNORECASE)
        # Strip all other HTML tags
        clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
        # Decode common HTML entities
        clean_text = clean_text.replace("&nbsp;", " ").replace("&amp;", "&")

        # Fallback Email Regex
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, clean_text)
        valid_emails = []
        for e in emails:
            e_lower = e.lower()
            if not any(e_lower.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]):
                valid_emails.append(e)

        # Fallback Phone Regex
        phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, clean_text)
        valid_phones = []
        for p in phones:
            digits_only = re.sub(r'\D', '', p)
            if 10 <= len(digits_only) <= 15:
                # Avoid solid long numbers without formatting (e.g. 1364148190886)
                # unless they start with '+' (which implies an international code format)
                if len(digits_only) == len(p.strip()) and not p.strip().startswith('+'):
                    continue
                valid_phones.append(p.strip())

        email = link_emails[0] if link_emails else (valid_emails[0] if valid_emails else None)
        phone = link_phones[0] if link_phones else (valid_phones[0] if valid_phones else None)

        return email, phone
    except Exception as e:
        print(f"Warning: Error extracting contact info from {url}: {e}")
        return None, None

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

        # Extract email & phone from website
        email, phone = None, None
        if website:
            print(f"Crawling website: {website} for contact details...")
            email, phone = extract_contact_info(website)

        leads.append({
            "name": name,
            "service": service,
            "address": address,
            "website": website if website else None,
            "rating": float(rating) if rating is not None else None,
            "email": email,
            "phone": phone,
            "date_created": today_str,
            "status": "lead"
        })

    return leads
