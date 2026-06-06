import os
import requests
import json
import modal
from fastapi import FastAPI, Request, Response

# 1. Define the Modal App & Image dependencies
image = (
    modal.Image.debian_slim()
    .pip_install("pyairtable", "google-generativeai", "requests")
)

app = modal.App(name="googlemaps-chatbot", image=image)
web_app = FastAPI()

# 2. Helper to send messages to Telegram
def send_telegram_message(token: str, chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

# 3. Helper to parse intent using Gemini
def parse_query_with_gemini(query: str, api_key: str) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    You are an intent parser for a Lead Generation Bot. The user can ask two types of queries:
    1. Lead generation: Scrape Google Maps and save leads (e.g. "Find 5 plumbers in Miami", "Scrape 10 dental clinics in Toronto").
    2. Lead search: Search already saved leads in Airtable (e.g. "Search for plumbers in Miami with minimum rating 4", "Find stored dentists in Toronto").
    
    Analyze the user query: "{query}"
    
    Respond ONLY with a JSON object in this format:
    For lead generation (scrape_leads):
    {{
      "intent": "scrape_leads",
      "service": "plumber",
      "city": "Miami",
      "count": 5
    }}
    
    For lead search (search_leads):
    {{
      "intent": "search_leads",
      "service": "plumber",
      "city": "Miami",
      "minimum_rating": 4.0,
      "status": "lead",
      "count": 5
    }}
    
    If you cannot determine the intent or details are missing, return:
    {{
      "intent": "unknown",
      "message": "A polite clarification message asking for the missing details"
    }}
    
    Do not include any markdown formatting (like ```json) in your response. Just return the raw JSON string.
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return {"intent": "unknown", "message": "Failed to parse query using Gemini."}

# 4. Webhook entry point
@web_app.post("/webhook")
async def telegram_webhook(request: Request):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    gemini_key = os.getenv("GEMINI_API_KEY")

    try:
        body = await request.json()
    except Exception:
        return Response(status_code=400)

    # Check for text message
    message = body.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")

    if not chat_id or not text:
        return Response(status_code=200)

    # 1. Parse using Gemini
    parsed = parse_query_with_gemini(text, gemini_key)
    intent = parsed.get("intent")

    if intent == "scrape_leads":
        service = parsed.get("service")
        city = parsed.get("city")
        count = parsed.get("count", 5)

        send_telegram_message(bot_token, chat_id, f"🔍 *Scraping Google Maps* for {count} '{service}' leads in {city}...")

        try:
            # Import local workflow execution files
            from execution.scrape_google_maps import scrape_google_maps
            from execution.airtable_save_leads import airtable_save_leads

            # Run Scrape
            leads = scrape_google_maps(service, city, count)
            if not leads:
                send_telegram_message(bot_token, chat_id, "⚠️ No leads found matching that search on Google Maps.")
                return Response(status_code=200)

            # Run Save to Airtable
            saved_count = airtable_save_leads(leads)

            # Review the top results
            review_text = f"✅ *Successfully saved {saved_count} leads to Airtable!*\n\nHere is a review of the top results:\n"
            for idx, lead in enumerate(leads, start=1):
                rating_str = f"⭐ {lead['rating']}" if lead['rating'] else "No rating"
                website_str = f"[Website]({lead['website']})" if lead['website'] else "No website"
                review_text += f"{idx}. *{lead['name']}* ({rating_str})\n   📍 {lead['address']}\n   🔗 {website_str}\n\n"

            send_telegram_message(bot_token, chat_id, review_text)

        except Exception as e:
            send_telegram_message(bot_token, chat_id, f"❌ *Error running scrape workflow*:\n`{str(e)}`")

    elif intent == "search_leads":
        service = parsed.get("service")
        city = parsed.get("city")
        min_rating = parsed.get("minimum_rating")
        status = parsed.get("status")
        count = parsed.get("count", 5)

        send_telegram_message(bot_token, chat_id, f"🔍 *Searching Airtable* for leads...")

        try:
            # Import local search execution file
            from execution.airtable_search_leads import airtable_search_leads

            # Run Search
            results = airtable_search_leads(city=city, service=service, minimum_rating=min_rating, status=status, count=count)
            if not results:
                send_telegram_message(bot_token, chat_id, "⚠️ No matching leads found in Airtable.")
                return Response(status_code=200)

            response_text = f"🔍 *Found {len(results)} matching leads in Airtable*:\n\n"
            for idx, lead in enumerate(results, start=1):
                rating_str = f"⭐ {lead['rating']}" if lead['rating'] else "No rating"
                website_str = f"[Website]({lead['website']})" if lead['website'] else "No website"
                response_text += f"{idx}. *{lead['name']}* ({rating_str})\n   📍 {lead['address']}\n   🔗 {website_str}\n\n"

            send_telegram_message(bot_token, chat_id, response_text)

        except Exception as e:
            send_telegram_message(bot_token, chat_id, f"❌ *Error running search workflow*:\n`{str(e)}`")

    else:
        # Default response or Gemini clarification message
        clarification = parsed.get("message", "I'm sorry, I didn't quite understand that. Try asking something like: 'Find 5 plumbers in Miami' or 'Search for plumbers in Miami with minimum rating 4'.")
        send_telegram_message(bot_token, chat_id, clarification)

    return Response(status_code=200)

# 5. Bind the web application & secrets to the Modal App
@app.function(
    secrets=[modal.Secret.from_name("googlemaps-secrets")],
    mounts=[
        modal.Mount.from_local_dir("d:\\SatishAIProjects\\05-GoogleMap\\execution", remote_path="/root/execution"),
    ]
)
@modal.asgi_app()
def fastapi_app():
    return web_app
