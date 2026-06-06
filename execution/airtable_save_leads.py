import os
from pyairtable import Api
from dotenv import load_dotenv

def airtable_save_leads(leads: list) -> int:
    """
    Saves a list of leads to Airtable.
    Each lead dictionary must have keys: name, service, address, website, rating, date_created, status.
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

    records_to_create = []
    for lead in leads:
        # Prepare fields matching columns exactly
        fields = {
            "name": lead.get("name"),
            "service": lead.get("service"),
            "address": lead.get("address"),
            "website": lead.get("website"),
            "rating": lead.get("rating"),
            "email": lead.get("email"),
            "phone_number": lead.get("phone"),
            "date_created": lead.get("date_created"),
            "status": lead.get("status", "lead")
        }
        records_to_create.append(fields)

    # pyairtable's batch_create handles lists of dicts and automatically
    # chunks them into groups of 10 (Airtable's limit) behind the scenes.
    created_records = table.batch_create(records_to_create)
    return len(created_records)
