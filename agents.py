import os
import requests
import wikipedia
from huggingface_hub import InferenceApi
from dotenv import load_dotenv

load_dotenv()

# Load API keys from .env
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
LOCATIONIQ_API_KEY = os.getenv("LOCATIONIQ_API_KEY")

# ===== 1. City Selector Agent =====
def city_selector_agent(interests, season):
    """Suggest cities based on interests and season."""
    cities_db = {
        "beach": ["Goa", "Maldives", "Bali"],
        "history": ["Rome", "Athens", "Varanasi"],
        "food": ["Bangkok", "Istanbul", "Mexico City"]
    }
    return cities_db.get(interests.lower(), ["London", "Paris", "Tokyo"])

# ===== 2. Local Expert Agent =====
def local_expert_agent(city):
    """Get cultural and attraction info from Wikipedia."""
    try:
        summary = wikipedia.summary(city, sentences=3)
    except:
        summary = "No cultural information found."
    return summary

# ===== 3. Trip Planner Agent =====
def trip_planner_agent(city):
    """Create a simple itinerary."""
    return [
        {"day": 1, "plan": f"Explore main landmarks in {city}"},
        {"day": 2, "plan": "Visit local markets and cultural sites"},
        {"day": 3, "plan": "Relax or take a nearby day trip"}
    ]

# ===== 4. Budget Manager Agent =====
def budget_manager_agent(budget_inr, days):
    """Simple budget allocation."""
    daily_budget = budget_inr / days
    return {
        "total_budget_inr": budget_inr,
        "daily_budget_inr": daily_budget
    }

# ===== 5. Flight Price Checker Agent =====
def flight_price_agent(departure_city, arrival_city):
    """Check flights using AviationStack API."""
    url = f"http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "dep_iata": departure_city,
        "arr_iata": arrival_city,
        "limit": 3
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        flights = []
        for flight in data.get("data", []):
            flights.append({
                "airline": flight["airline"]["name"],
                "flight_number": flight["flight"]["iata"],
                "departure": flight["departure"]["scheduled"],
                "arrival": flight["arrival"]["scheduled"]
            })
        return flights
    except Exception as e:
        return [{"error": str(e)}]

# ===== 6. Chatbot Refinement Agent =====
def chatbot_agent(prompt):
    """Refine itinerary using Hugging Face model."""
    hf_api = InferenceApi(repo_id="mistralai/Mistral-7B-Instruct", token=HUGGINGFACE_API_KEY)
    try:
        response = hf_api(prompt)
        if isinstance(response, list):
            return response[0].get("generated_text", "No response")
        elif isinstance(response, dict):
            return response.get("generated_text", "No response")
        else:
            return str(response)
    except Exception as e:
        return f"Chatbot error: {str(e)}"

# ===== 7. LocationIQ Geocoding Agent =====
def geocode_city(city):
    """Get latitude & longitude from LocationIQ."""
    url = f"https://us1.locationiq.com/v1/search"
    params = {
        "key": LOCATIONIQ_API_KEY,
        "q": city,
        "format": "json"
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        return None, None
