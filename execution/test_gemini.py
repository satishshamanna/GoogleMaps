import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

def test_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"Gemini API Key loaded (first 5 chars): {api_key[:5] if api_key else 'None'}")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return
        
    # Initialize the new SDK client
    client = genai.Client(api_key=api_key)
    
    print("\nAttempting basic generate_content call with 'gemini-3.5-flash' using google-genai...")
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents="Say hello in one word."
        )
        print(f"Response: '{response.text.strip()}'")
    except Exception as e:
        print(f"Failed to generate content: {e}")

if __name__ == "__main__":
    test_gemini()
