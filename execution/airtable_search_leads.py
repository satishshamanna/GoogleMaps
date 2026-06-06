import os
from pyairtable import Api
from dotenv import load_dotenv

def airtable_search_leads(city: str = None, service: str = None, minimum_rating: float = None, status: str = None, count: int = 5) -> list:
    """
    Queries Airtable with optional filters (city, service, minimum_rating, status)
    and returns up to `count` records sorted by rating descending.
    """
    load_dotenv()
    api_token = os.getenv("AIRTABLE_API_TOKEN")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME", "Leads")

    if not api_token or api_token == "your_airtable_pat":
        raise ValueError("AIRTABLE_API_TOKEN is not set or has a placeholder value in .env.")
    if not base_id or base_id == "your_base_id":
        raise ValueError("AIRTABLE_BASE_ID is not set or has a placeholder value in .env.")

    api = Api(api_token)
    table = api.table(base_id, table_name)

    # Build Airtable filter formula
    filters = []
    if city:
        escaped_city = city.replace('"', '\\"')
        filters.append(f"FIND(LOWER(\"{escaped_city}\"), LOWER({{address}}))")
    if service:
        escaped_service = service.replace('"', '\\"')
        filters.append(f"LOWER({{service}}) = LOWER(\"{escaped_service}\")")
    if minimum_rating is not None:
        try:
            val = float(minimum_rating)
            filters.append(f"{{rating}} >= {val}")
        except ValueError:
            pass
    if status:
        escaped_status = status.replace('"', '\\"')
        filters.append(f"LOWER({{status}}) = LOWER(\"{escaped_status}\")")

    formula = None
    if filters:
        if len(filters) == 1:
            formula = filters[0]
        else:
            formula = f"AND({', '.join(filters)})"

    # Query table. Sort by rating descending.
    # Note: fields are sorted using pyairtable's sort parameter.
    records = table.all(formula=formula, sort=["-rating"])

    # Format output list of lead dicts
    results = []
    for record in records:
        fields = record.get("fields", {})
        results.append({
            "id": record.get("id"),
            "name": fields.get("name"),
            "service": fields.get("service"),
            "address": fields.get("address"),
            "website": fields.get("website"),
            "rating": fields.get("rating"),
            "date_created": fields.get("date_created"),
            "status": fields.get("status")
        })

    # Slices output to match count
    return results[:count]
